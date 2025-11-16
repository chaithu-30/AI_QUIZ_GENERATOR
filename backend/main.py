from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime

from database import get_db, init_db, Quiz, test_connection
from models import QuizGenerateRequest, QuizHistoryItem
from scraper import scrape_wikipedia, validate_wikipedia_url
from llm_quiz_generator import generate_quiz_from_article
from config import settings

# Validate configuration on startup
settings.validate()

# Initialize FastAPI app
app = FastAPI(
    title="AI Wiki Quiz Generator",
    description="Generate AI-powered quizzes from Wikipedia articles using Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CRITICAL: CORS Configuration - Must be BEFORE all route definitions
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://ai-quiz-generator-git-master-chaithanyas-projects-392bdd1f.vercel.app",
        "https://ai-quiz-generator.vercel.app",
        "https://*.vercel.app",
        "*"  # Allow all origins - remove in production after testing
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ],
    expose_headers=["*"],
    max_age=3600,
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and test connections on startup"""
    print("\n" + "="*50)
    print("Starting AI Wiki Quiz Generator")
    print("="*50)
    
    if test_connection():
        init_db()
    else:
        print("Warning: Database connection issues detected")
    
    print(f"Server running on {settings.HOST}:{settings.PORT}")
    print(f"Debug mode: {settings.DEBUG}")
    print("="*50 + "\n")

# Root endpoint
@app.get("/")
async def root():
    """API Root - Welcome message and endpoint list"""
    return {
        "message": "AI Wiki Quiz Generator API",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "POST /api/generate_quiz/",
            "get_history": "GET /api/history/",
            "get_quiz_details": "GET /api/quiz/{id}/",
            "health_check": "GET /health"
        },
        "docs": "/docs",
        "cors": "enabled"
    }

# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Check if API and database are healthy"""
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat(),
            "cors": "enabled"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# ENDPOINT 1: Generate Quiz
@app.post("/api/generate_quiz/")
async def generate_quiz(
    request: QuizGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate quiz from Wikipedia URL with caching support
    
    Request Body:
    - url: Wikipedia article URL (required)
    - force: Force regenerate even if cached (optional, default: false)
    
    Returns:
    - Complete quiz data with questions, entities, and related topics
    """
    try:
        # Validate URL format
        if not validate_wikipedia_url(request.url):
            raise HTTPException(
                status_code=400,
                detail="Invalid Wikipedia URL. Must be https://en.wikipedia.org/wiki/Article_Name"
            )
        
        # Check cache
        existing_quiz = db.query(Quiz).filter(Quiz.url == request.url).first()
        
        if existing_quiz and not request.force:
            print(f"✓ Returning cached quiz for: {request.url}")
            quiz_data = json.loads(existing_quiz.full_quiz_data)
            return {
                "id": existing_quiz.id,
                "url": existing_quiz.url,
                "cached": True,
                "date_generated": existing_quiz.date_generated.isoformat(),
                **quiz_data
            }
        
        # Step 1: Scrape Wikipedia
        print(f"→ Scraping Wikipedia: {request.url}")
        try:
            title, clean_text, raw_html = scrape_wikipedia(request.url)
            print(f"✓ Scraped: {title} ({len(clean_text)} characters)")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")
        
        # Step 2: Generate quiz with LLM
        print(f"→ Generating quiz with Gemini AI...")
        try:
            quiz_data = generate_quiz_from_article(title, clean_text)
            print(f"✓ Generated {len(quiz_data['quiz'])} questions")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")
        
        # Step 3: Save to database
        try:
            if existing_quiz:
                existing_quiz.full_quiz_data = json.dumps(quiz_data)
                existing_quiz.scraped_content = raw_html[:50000]
                existing_quiz.date_generated = datetime.utcnow()
                db.commit()
                quiz_id = existing_quiz.id
                print(f"✓ Updated quiz ID: {quiz_id}")
            else:
                new_quiz = Quiz(
                    url=request.url,
                    title=title,
                    full_quiz_data=json.dumps(quiz_data),
                    scraped_content=raw_html[:50000]
                )
                db.add(new_quiz)
                db.commit()
                db.refresh(new_quiz)
                quiz_id = new_quiz.id
                print(f"✓ Saved new quiz ID: {quiz_id}")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
        # Return success response
        return {
            "id": quiz_id,
            "url": request.url,
            "cached": False,
            "date_generated": datetime.utcnow().isoformat(),
            **quiz_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# ENDPOINT 2: Get Quiz History
@app.get("/api/history/", response_model=List[QuizHistoryItem])
async def get_history(db: Session = Depends(get_db)):
    """
    Get list of all generated quizzes
    
    Returns:
    - List of quiz summary objects (id, url, title, date_generated)
    """
    try:
        quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
        print(f"✓ Returning {len(quizzes)} quizzes from history")
        return quizzes
    except Exception as e:
        print(f"✗ Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ENDPOINT 3: Get Quiz Details
@app.get("/api/quiz/{quiz_id}/")
async def get_quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get complete quiz data for specific quiz ID
    
    Parameters:
    - quiz_id: Database ID of the quiz
    
    Returns:
    - Complete quiz data including questions, entities, and related topics
    """
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(
                status_code=404,
                detail=f"Quiz with ID {quiz_id} not found"
            )
        
        # Deserialize JSON data
        try:
            quiz_data = json.loads(quiz.full_quiz_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Corrupted quiz data in database")
        
        print(f"✓ Retrieved quiz ID: {quiz_id} - {quiz.title}")
        
        return {
            "id": quiz.id,
            "url": quiz.url,
            "date_generated": quiz.date_generated.isoformat(),
            "full_quiz_data": quiz_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error fetching quiz: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# OPTIONS handler for CORS preflight (explicit)
@app.options("/api/generate_quiz/")
async def options_generate_quiz():
    """Handle preflight OPTIONS request for generate_quiz endpoint"""
    return {"message": "OK"}

@app.options("/api/history/")
async def options_history():
    """Handle preflight OPTIONS request for history endpoint"""
    return {"message": "OK"}

@app.options("/api/quiz/{quiz_id}/")
async def options_quiz_details(quiz_id: int):
    """Handle preflight OPTIONS request for quiz details endpoint"""
    return {"message": "OK"}

# Exception handler for validation errors
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    """Handle validation errors with user-friendly messages"""
    return {
        "error": "Invalid Request",
        "message": "Please check your input data format",
        "details": str(exc)
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Catch-all exception handler"""
    print(f"✗ Unhandled exception: {str(exc)}")
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "details": str(exc) if settings.DEBUG else "Error details hidden in production"
    }
