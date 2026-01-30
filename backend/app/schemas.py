"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict
from datetime import datetime


# Quiz Question Schema
class QuizQuestion(BaseModel):
    """Individual quiz question schema."""
    question: str
    options: List[str] = Field(..., min_length=4, max_length=4)
    answer: str
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    explanation: str


# Key Entities Schema
class KeyEntities(BaseModel):
    """Key entities extracted from the article."""
    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []


# Request Schemas
class QuizGenerateRequest(BaseModel):
    """Request schema for quiz generation."""
    url: str = Field(..., description="Wikipedia article URL")


# Response Schemas
class QuizResponse(BaseModel):
    """Full quiz response schema matching the sample API output."""
    id: int
    url: str
    title: str
    summary: Optional[str] = None
    key_entities: Optional[KeyEntities] = None
    sections: Optional[List[str]] = None
    quiz: List[QuizQuestion]
    related_topics: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class QuizListItem(BaseModel):
    """Simplified quiz item for history list."""
    id: int
    url: str
    title: str
    question_count: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class QuizHistoryResponse(BaseModel):
    """Response schema for quiz history."""
    quizzes: List[QuizListItem]
    total: int


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    error_code: Optional[str] = None
