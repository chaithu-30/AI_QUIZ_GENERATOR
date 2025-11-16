from pydantic import BaseModel, Field, field_validator
from typing import List, Dict
from datetime import datetime

# Schema for individual quiz questions
class QuizQuestion(BaseModel):
    question: str = Field(..., description="The quiz question text")
    options: List[str] = Field(..., min_length=4, max_length=4, description="Four answer options")
    answer: str = Field(..., description="The correct answer")
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$", description="Question difficulty level")
    explanation: str = Field(..., description="Explanation for the answer")
    
    @field_validator('options')
    @classmethod
    def validate_options_unique(cls, v):
        """Ensure all options are unique"""
        if len(v) != len(set(v)):
            raise ValueError('All options must be unique')
        return v

# Schema for key entities extracted from article
class KeyEntities(BaseModel):
    people: List[str] = Field(default_factory=list)
    organizations: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)

# Complete quiz output schema
class QuizOutput(BaseModel):
    title: str = Field(..., description="Article title")
    summary: str = Field(..., min_length=50, description="Brief article summary")
    key_entities: KeyEntities
    sections: List[str] = Field(..., min_length=1, description="Main article sections")
    quiz: List[QuizQuestion] = Field(..., min_length=5, max_length=10)
    related_topics: List[str] = Field(..., min_length=3, description="Related Wikipedia topics")

# Request schema for quiz generation
class QuizGenerateRequest(BaseModel):
    url: str = Field(..., pattern="^https://en\\.wikipedia\\.org/wiki/.+$")
    force: bool = Field(default=False, description="Force regenerate even if exists")

# Response schema for history endpoint
class QuizHistoryItem(BaseModel):
    id: int
    url: str
    title: str
    date_generated: datetime
    
    class Config:
        from_attributes = True

# Response schema for quiz details
class QuizDetailResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict
    sections: List[str]
    quiz: List[Dict]
    related_topics: List[str]
