from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

# Input model for quiz generation request
class QuizGenerateRequest(BaseModel):
    url: str = Field(..., description="Wikipedia article URL")
    force: bool = Field(default=False, description="Force regenerate even if cached")

# Output model for quiz history items
class QuizHistoryItem(BaseModel):
    id: int
    url: str
    title: str
    date_generated: datetime
    
    class Config:
        from_attributes = True

# Individual quiz question schema
class QuizQuestion(BaseModel):
    question: str = Field(..., description="The quiz question text")
    options: List[str] = Field(..., description="Four answer options (A-D)", min_length=4, max_length=4)
    answer: str = Field(..., description="The correct answer")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(..., description="Brief explanation with article reference")

# Key entities extracted from article
class KeyEntities(BaseModel):
    people: List[str] = Field(default_factory=list, description="People mentioned in the article")
    organizations: List[str] = Field(default_factory=list, description="Organizations mentioned")
    locations: List[str] = Field(default_factory=list, description="Locations mentioned")

# Complete quiz output schema
class QuizOutput(BaseModel):
    title: str = Field(..., description="Article title")
    summary: str = Field(..., description="Brief 2-3 sentence summary")
    key_entities: KeyEntities = Field(..., description="Extracted key entities")
    sections: List[str] = Field(..., description="Main article sections")
    quiz: List[QuizQuestion] = Field(..., description="List of quiz questions", min_length=5, max_length=10)
    related_topics: List[str] = Field(..., description="Related Wikipedia topics", min_length=3, max_length=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python (programming language)",
                "summary": "Python is a high-level programming language...",
                "key_entities": {
                    "people": ["Guido van Rossum"],
                    "organizations": ["Python Software Foundation"],
                    "locations": ["Netherlands"]
                },
                "sections": ["History", "Design philosophy", "Syntax"],
                "quiz": [
                    {
                        "question": "Who created Python?",
                        "options": ["Guido van Rossum", "Linus Torvalds", "James Gosling", "Dennis Ritchie"],
                        "answer": "Guido van Rossum",
                        "difficulty": "easy",
                        "explanation": "Mentioned in the History section."
                    }
                ],
                "related_topics": ["Programming language", "Software development", "Computer science"]
            }
        }
