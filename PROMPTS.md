# LangChain Prompt Templates

This document contains the LangChain prompt templates used for quiz generation and related topic suggestion.

## Quiz Generation Prompt

```python
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
```

### Key Design Decisions

1. **Explicit Grounding**: The prompt emphasizes generating questions "based ONLY on facts explicitly stated in the article" to minimize hallucination.

2. **Structured Output**: Requesting JSON output with a specific schema ensures consistent parsing.

3. **Difficulty Distribution**: Clear definitions of difficulty levels ensure a balanced quiz.

4. **Explanation Requirement**: Forcing explanations to reference article sections creates transparency.

5. **Plausible Distractors**: Instructions to make incorrect options "plausible but clearly wrong" improves quiz quality.

---

## Related Topics Prompt

```python
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
```

### Key Design Decisions

1. **Context Provision**: Including sections and entities helps the LLM understand the article's scope.

2. **Wikipedia-Specific**: Requesting topics that could be Wikipedia article titles ensures practical suggestions.

3. **Diversity**: Asking for 5-7 topics provides variety without overwhelming users.

4. **Relevance Filter**: The instruction to suggest "directly connected" topics ensures relevance.

---

## Implementation Notes

### Model Selection
- Using `llama-3.1-8b-instant` from Groq for fast, capable responses
- Temperature set to 0.3 for more deterministic, factual outputs

### Content Truncation
- Article content is truncated to ~12,000 characters to fit within token limits
- Truncation preserves paragraph boundaries when possible

### JSON Parsing
- Response parsing handles multiple formats:
  - Direct JSON
  - JSON in markdown code blocks
  - JSON embedded in text

### Validation
- Quiz questions are validated for:
  - Required fields (question, options, answer, difficulty, explanation)
  - Exactly 4 options per question
  - Valid difficulty levels (easy, medium, hard)

---

## Anti-Hallucination Strategies

1. **Source Grounding**: Emphasizing that questions must be based on article content
2. **Explanation Requirement**: Forcing citations to article sections
3. **Low Temperature**: Using 0.3 temperature for more deterministic outputs
4. **Validation Layer**: Post-processing validation of generated content
5. **Clear Constraints**: Explicit instructions about what NOT to do
