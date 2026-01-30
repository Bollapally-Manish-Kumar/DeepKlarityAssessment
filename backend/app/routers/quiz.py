"""Quiz API router with endpoints for quiz generation and history."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import logging
import traceback

from ..database import get_db
from ..models import Quiz
from ..schemas import (
    QuizGenerateRequest,
    QuizResponse,
    QuizListItem,
    QuizHistoryResponse,
    KeyEntities,
    QuizQuestion
)
from ..services.scraper import scrape_wikipedia
from ..services.llm_service import generate_quiz, generate_related_topics

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def generate_quiz_endpoint(request: QuizGenerateRequest, db: Session = Depends(get_db)):
    """
    Generate a quiz from a Wikipedia article URL.
    
    - Scrapes the Wikipedia article content
    - Uses LLM to generate quiz questions
    - Stores the result in the database
    - Returns the full quiz data
    """
    url = request.url.strip()
    
    # Check if quiz already exists for this URL (caching)
    existing_quiz = db.query(Quiz).filter(Quiz.url == url).first()
    if existing_quiz:
        logger.info(f"Returning cached quiz for URL: {url}")
        return _quiz_to_response(existing_quiz)
    
    try:
        # Step 1: Scrape the Wikipedia article
        logger.info(f"Scraping Wikipedia article: {url}")
        scraped_data = scrape_wikipedia(url)
        logger.info(f"Scraped article: {scraped_data['title']}, content length: {len(scraped_data['content'])}")
        
        # Step 2: Generate quiz using LLM
        logger.info(f"Generating quiz for: {scraped_data['title']}")
        quiz_questions = generate_quiz(
            title=scraped_data["title"],
            content=scraped_data["content"],
            num_questions=7
        )
        logger.info(f"Generated {len(quiz_questions)} questions")
        
        if not quiz_questions:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate quiz questions. Please try again."
            )
        
        # Step 3: Generate related topics
        logger.info("Generating related topics")
        related_topics = generate_related_topics(
            title=scraped_data["title"],
            sections=scraped_data["sections"],
            entities=scraped_data["key_entities"]
        )
        logger.info(f"Generated {len(related_topics)} related topics")
        
        # Step 4: Store in database
        logger.info("Storing quiz in database")
        quiz = Quiz(
            url=url,
            title=scraped_data["title"],
            summary=scraped_data["summary"],
            key_entities=scraped_data["key_entities"],
            sections=scraped_data["sections"],
            quiz_data=quiz_questions,
            related_topics=related_topics,
            raw_html=scraped_data["raw_html"]
        )
        
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        
        logger.info(f"Quiz created with ID: {quiz.id}")
        return _quiz_to_response(quiz)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError:
        db.rollback()
        # Race condition - quiz was created by another request
        existing_quiz = db.query(Quiz).filter(Quiz.url == url).first()
        if existing_quiz:
            return _quiz_to_response(existing_quiz)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error. Please try again."
        )
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )


@router.get("/history", response_model=QuizHistoryResponse)
async def get_quiz_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get list of all previously generated quizzes.
    
    - Returns paginated list of quizzes
    - Ordered by creation date (newest first)
    """
    # Get total count
    total = db.query(Quiz).count()
    
    # Get quizzes with pagination
    quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).offset(skip).limit(limit).all()
    
    quiz_items = [
        QuizListItem(
            id=q.id,
            url=q.url,
            title=q.title,
            question_count=len(q.quiz_data) if q.quiz_data else 0,
            created_at=q.created_at
        )
        for q in quizzes
    ]
    
    return QuizHistoryResponse(quizzes=quiz_items, total=total)


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific quiz by ID.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with ID {quiz_id} not found"
        )
    
    return _quiz_to_response(quiz)


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Delete a quiz by ID.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with ID {quiz_id} not found"
        )
    
    db.delete(quiz)
    db.commit()
    return None


def _quiz_to_response(quiz: Quiz) -> QuizResponse:
    """Convert Quiz model to QuizResponse schema."""
    key_entities = None
    if quiz.key_entities:
        key_entities = KeyEntities(
            people=quiz.key_entities.get("people", []),
            organizations=quiz.key_entities.get("organizations", []),
            locations=quiz.key_entities.get("locations", [])
        )
    
    quiz_questions = []
    if quiz.quiz_data:
        for q in quiz.quiz_data:
            quiz_questions.append(QuizQuestion(
                question=q.get("question", ""),
                options=q.get("options", []),
                answer=q.get("answer", ""),
                difficulty=q.get("difficulty", "medium"),
                explanation=q.get("explanation", "")
            ))
    
    return QuizResponse(
        id=quiz.id,
        url=quiz.url,
        title=quiz.title,
        summary=quiz.summary,
        key_entities=key_entities,
        sections=quiz.sections,
        quiz=quiz_questions,
        related_topics=quiz.related_topics,
        created_at=quiz.created_at
    )
