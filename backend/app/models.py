"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class Quiz(Base):
    """Quiz model for storing generated quizzes from Wikipedia articles."""
    
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), nullable=False, unique=True, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    key_entities = Column(JSON, nullable=True)  # {"people": [], "organizations": [], "locations": []}
    sections = Column(JSON, nullable=True)  # ["Section 1", "Section 2", ...]
    quiz_data = Column(JSON, nullable=False)  # List of quiz questions
    related_topics = Column(JSON, nullable=True)  # List of related topic strings
    raw_html = Column(Text, nullable=True)  # Store raw HTML for reference
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"
