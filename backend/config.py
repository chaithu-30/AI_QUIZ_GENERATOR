import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration settings"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS - Allow Vercel
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "")
    ]
    
    # Scraping
    REQUEST_TIMEOUT: int = 15
    MAX_CONTENT_LENGTH: int = 5000
    
    # LLM
    LLM_TEMPERATURE: float = 0.3
    LLM_MODEL: str = "models/gemini-2.5-flash"
    
    def validate(self):
        """Validate required settings"""
        errors = []
        
        if not self.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required")
        
        if not self.DATABASE_URL:
            errors.append("DATABASE_URL is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True

settings = Settings()
