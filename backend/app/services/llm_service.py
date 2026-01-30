"""LLM service for quiz generation using LangChain and Groq."""
import json
import re
import logging
from typing import Dict, List, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from ..config import get_settings

logger = logging.getLogger(__name__)


# Pydantic models for structured output
class QuizQuestionModel(BaseModel):
    """Model for a single quiz question."""
    question: str = Field(description="The question text")
    options: List[str] = Field(description="Four possible answers (A, B, C, D)")
    answer: str = Field(description="The correct answer (must match one of the options)")
    difficulty: str = Field(description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(description="Brief explanation referencing the article")


class QuizOutputModel(BaseModel):
    """Model for the complete quiz output."""
    quiz: List[QuizQuestionModel] = Field(description="List of quiz questions")


class RelatedTopicsModel(BaseModel):
    """Model for related topics output."""
    topics: List[str] = Field(description="List of related topic names")


# Prompt templates
QUIZ_GENERATION_PROMPT = """You are an expert quiz generator specializing in educational content. Your task is to create a high-quality quiz based on the following Wikipedia article.

**Article Title:** {title}

**Article Content:**
{content}

**Instructions:**
1. Generate exactly {num_questions} quiz questions based ONLY on facts explicitly stated in the article.
2. Each question must have exactly 4 options (A, B, C, D) with only ONE correct answer.
3. Include a mix of difficulty levels:
   - "easy": Basic facts directly stated in the article
   - "medium": Requires understanding of concepts or relationships
   - "hard": Requires synthesis of multiple facts or deeper comprehension
4. Each explanation should reference the specific section or context from the article.
5. NEVER make up facts that aren't in the article.
6. Ensure the correct answer is clearly stated in the article content.
7. Make incorrect options plausible but clearly wrong based on the article.

**Output Format:**
Return a valid JSON object with the following structure:
{{
    "quiz": [
        {{
            "question": "Question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "The correct option text (must exactly match one of the options)",
            "difficulty": "easy|medium|hard",
            "explanation": "Brief explanation referencing the article section."
        }}
    ]
}}

Generate the quiz now:"""


RELATED_TOPICS_PROMPT = """Based on the following Wikipedia article, suggest related topics that would help readers deepen their understanding of the subject.

**Article Title:** {title}

**Article Sections:** {sections}

**Key Entities:**
- People: {people}
- Organizations: {organizations}
- Locations: {locations}

**Instructions:**
1. Suggest 5-7 related topics that are directly connected to this article's subject.
2. Include topics that provide context, background, or related concepts.
3. Topics should be specific enough to be Wikipedia article titles.
4. Avoid suggesting the same topic as the article title.

**Output Format:**
Return a valid JSON object:
{{
    "topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
}}

Generate related topics now:"""


# Initialize prompt templates at module level
QUIZ_PROMPT_TEMPLATE = ChatPromptTemplate.from_template(QUIZ_GENERATION_PROMPT)
RELATED_TOPICS_TEMPLATE = ChatPromptTemplate.from_template(RELATED_TOPICS_PROMPT)


class LLMService:
    """Service for generating quizzes using LLM."""
    
    def __init__(self):
        self._llm = None
    
    def _get_llm(self):
        """Lazy initialization of LLM client."""
        if self._llm is None:
            settings = get_settings()
            logger.info(f"Initializing Groq LLM...")
            self._llm = ChatGroq(
                api_key=settings.groq_api_key,
                model_name="llama-3.1-8b-instant",
                temperature=0.3,
                max_tokens=4096
            )
        return self._llm
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from LLM response, handling common issues."""
        text = response.strip()
        logger.debug(f"Parsing LLM response: {text[:500]}")
        
        # Try direct parsing first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in markdown code blocks
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON object in the text
        json_match = re.search(r"\{[\s\S]*\}", text)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        raise ValueError(f"Could not parse JSON from response: {text[:500]}")
    
    def _truncate_content(self, content: str, max_chars: int = 10000) -> str:
        """Truncate content to fit within token limits."""
        if len(content) <= max_chars:
            return content
        
        # Try to truncate at a paragraph boundary
        truncated = content[:max_chars]
        last_para = truncated.rfind("\n\n")
        if last_para > max_chars * 0.7:
            return truncated[:last_para] + "\n\n[Content truncated for length...]"
        return truncated + "\n\n[Content truncated for length...]"
    
    def generate_quiz(self, title: str, content: str, num_questions: int = 7) -> List[Dict]:
        """Generate quiz questions from article content."""
        try:
            llm = self._get_llm()
            
            # Truncate content to avoid token limits
            truncated_content = self._truncate_content(content)
            logger.info(f"Generating quiz for '{title}' with {len(truncated_content)} chars of content")
            
            # Create the prompt
            messages = QUIZ_PROMPT_TEMPLATE.format_messages(
                title=title,
                content=truncated_content,
                num_questions=num_questions
            )
            
            # Generate response
            logger.info("Calling Groq API for quiz generation...")
            response = llm.invoke(messages)
            logger.info(f"Received response with {len(response.content)} chars")
            
            # Parse the response
            parsed = self._parse_json_response(response.content)
            
            # Validate and clean quiz questions
            quiz = parsed.get("quiz", [])
            valid_questions = []
            
            for q in quiz:
                # Ensure all required fields exist
                if all(key in q for key in ["question", "options", "answer", "difficulty", "explanation"]):
                    # Validate options count
                    if len(q["options"]) == 4:
                        # Normalize difficulty
                        q["difficulty"] = q["difficulty"].lower()
                        if q["difficulty"] not in ["easy", "medium", "hard"]:
                            q["difficulty"] = "medium"
                        valid_questions.append(q)
            
            logger.info(f"Generated {len(valid_questions)} valid questions")
            return valid_questions
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}", exc_info=True)
            raise
    
    def generate_related_topics(self, title: str, sections: List[str], entities: Dict) -> List[str]:
        """Generate related topics for further reading."""
        try:
            llm = self._get_llm()
            
            # Create the prompt
            messages = RELATED_TOPICS_TEMPLATE.format_messages(
                title=title,
                sections=", ".join(sections[:10]) if sections else "N/A",
                people=", ".join(entities.get("people", [])[:5]) if entities.get("people") else "N/A",
                organizations=", ".join(entities.get("organizations", [])[:5]) if entities.get("organizations") else "N/A",
                locations=", ".join(entities.get("locations", [])[:5]) if entities.get("locations") else "N/A"
            )
            
            # Generate response
            logger.info("Calling Groq API for related topics...")
            response = llm.invoke(messages)
            
            # Parse the response
            parsed = self._parse_json_response(response.content)
            
            # Extract topics
            topics = parsed.get("topics", [])
            
            # Filter out the article title itself
            topics = [t for t in topics if t.lower() != title.lower()]
            
            logger.info(f"Generated {len(topics)} related topics")
            return topics[:7]
            
        except Exception as e:
            logger.error(f"Error generating related topics: {str(e)}", exc_info=True)
            # Return empty list instead of failing
            return []


# Singleton instance
llm_service = LLMService()


def generate_quiz(title: str, content: str, num_questions: int = 7) -> List[Dict]:
    """Convenience function to generate a quiz."""
    return llm_service.generate_quiz(title, content, num_questions)


def generate_related_topics(title: str, sections: List[str], entities: Dict) -> List[str]:
    """Convenience function to generate related topics."""
    return llm_service.generate_related_topics(title, sections, entities)
