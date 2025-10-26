from pydantic import BaseModel, Field
from typing import List, Optional

class QuizQuestion(BaseModel):
    """Schema for a single quiz question"""
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., min_length=4, max_length=4, 
                               description="Exactly 4 answer options (A-D)")
    answer: str = Field(..., description="The correct answer")
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$",
                           description="Difficulty level")
    explanation: str = Field(..., description="Short explanation with section reference")

class KeyEntities(BaseModel):
    """Schema for key entities extracted from article"""
    people: List[str] = Field(default_factory=list)
    organizations: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)

class QuizOutput(BaseModel):
    """Complete schema for LLM output - enforces structure"""
    title: str
    summary: str = Field(..., max_length=500, description="Brief article summary")
    key_entities: KeyEntities
    sections: List[str] = Field(..., description="Main article sections")
    quiz: List[QuizQuestion] = Field(..., min_length=5, max_length=10,
                                     description="5-10 quiz questions")
    related_topics: List[str] = Field(..., min_length=3, max_length=8,
                                      description="3-8 related Wikipedia topics")
