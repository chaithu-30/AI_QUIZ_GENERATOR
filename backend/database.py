from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Create engine with production settings
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Important for Render deployment
    connect_args={
        "connect_timeout": 30,
        "read_timeout": 60,
        "write_timeout": 60,
        "charset": "utf8mb4"
    },
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Quiz Model
class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    date_generated = Column(DateTime, default=datetime.utcnow)
    scraped_content = Column(Text, nullable=True)
    full_quiz_data = Column(Text, nullable=False)
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"

# Initialize database tables
def init_db():
    """Create all tables in the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database connected successfully")
        print("Tables created/verified")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise

# Dependency for FastAPI
def get_db():
    """Provides a database session for each request"""
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        yield db
    except Exception as e:
        print(f"Database connection error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Test database connection
def test_connection():
    """Test if database connection is working"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            if row and row[0] == 1:
                print("Database connection test successful")
                return True
            else:
                print("Unexpected result from database")
                return False
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
