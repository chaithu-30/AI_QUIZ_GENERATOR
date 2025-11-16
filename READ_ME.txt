# AI Wiki Quiz Generator - Production README

## Live Deployment

**Application is live and fully functional:**
- Frontend: https://ai-quiz-generator-pink.vercel.app
- Backend API: https://ai-quiz-generator-c20h.onrender.com
- API Documentation: https://ai-quiz-generator-c20h.onrender.com/docs
- Health Check: https://ai-quiz-generator-c20h.onrender.com/health

## Project Overview

This is a production-ready full-stack application that generates AI-powered quizzes from Wikipedia articles using Google Gemini 2.5 Flash and FastAPI. The system automatically scrapes Wikipedia content, processes it with a Large Language Model, and presents interactive quizzes with detailed explanations.

## Technical Stack

### Backend
- Python 3.13
- FastAPI web framework
- SQLAlchemy ORM with Railway MySQL
- Google Generative AI (Gemini 2.5 Flash)
- BeautifulSoup4 for web scraping
- Pydantic for data validation

### Frontend
- React 18
- Tailwind CSS
- Axios for HTTP requests
- Responsive design

### Deployment
- Backend: Render (https://render.com)
- Frontend: Vercel (https://vercel.com)
- Database: Railway MySQL (https://railway.app)

## Core Features

### Implemented Features
1. AI-powered quiz generation from any Wikipedia article
2. Automatic extraction of article content and key entities
3. 7-10 multiple choice questions with difficulty levels (easy, medium, hard)
4. Detailed explanations for each answer
5. Related topics suggestions
6. Quiz history with persistent storage
7. Caching system to prevent duplicate processing
8. URL validation for Wikipedia articles
9. Interactive "Take Quiz" mode with scoring
10. Raw HTML storage in database
11. Clean, responsive UI with Tailwind CSS
12. Comprehensive error handling

### Bonus Features Implemented
- URL validation
- Quiz caching (duplicate URL detection)
- Raw HTML storage for reference
- Interactive "Take Quiz" mode with user scoring
- Minimal, professional UI design
- Section-wise organization in quiz display

## API Documentation

### Base URLs
- Production API: https://ai-quiz-generator-c20h.onrender.com
- API Endpoints: https://ai-quiz-generator-c20h.onrender.com/api/

### Endpoints

#### 1. POST /api/generate_quiz/
Generate a new quiz from Wikipedia URL.

**Request:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "force": false
}
```

**Response:**
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "cached": false,
  "date_generated": "2025-11-16T15:30:00",
  "title": "Python (programming language)",
  "summary": "Python is a high-level, general-purpose programming language...",
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
  "related_topics": ["Programming language", "Software development"]
}
```

#### 2. GET /api/history/
Retrieve list of all generated quizzes.

**Response:**
```json
[
  {
    "id": 1,
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "title": "Python (programming language)",
    "date_generated": "2025-11-16T15:30:00"
  }
]
```

#### 3. GET /api/quiz/{quiz_id}/
Get specific quiz details by ID.

**Response:**
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "date_generated": "2025-11-16T15:30:00",
  "full_quiz_data": {
    "title": "...",
    "summary": "...",
    "quiz": [...]
  }
}
```

#### 4. GET /health
Check API health status.

#### 5. GET /docs
Interactive API documentation (Swagger UI).

## Database Schema

### Quiz Table Structure

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| url | String(500) | Wikipedia article URL (unique) |
| title | String(255) | Article title |
| date_generated | DateTime | Quiz creation timestamp |
| scraped_content | Text | Raw HTML content (first 50,000 chars) |
| full_quiz_data | Text | Complete quiz data as JSON string |

## LLM Prompt Template

The system uses a carefully designed prompt to ensure high-quality, factually accurate quiz generation:

```
You are an expert educational content creator. Generate a comprehensive quiz 
based STRICTLY on the Wikipedia article provided.

STRICT RULES:
- Use ONLY information from the article text below
- DO NOT use external knowledge
- Every question must be answerable from the article
- Include section references in explanations
- Ensure diverse difficulty levels (easy, medium, hard)

ARTICLE TITLE: {title}
ARTICLE TEXT: {article_text}

YOUR TASK:
Generate a quiz with the following structure in pure JSON format:

{
  "title": "Article Title",
  "summary": "Brief 2-3 sentence summary",
  "key_entities": {
    "people": ["Person 1", "Person 2"],
    "organizations": ["Org 1", "Org 2"],
    "locations": ["Location 1", "Location 2"]
  },
  "sections": ["Section 1", "Section 2", "Section 3"],
  "quiz": [
    {
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option",
      "difficulty": "easy",
      "explanation": "Explanation with article reference"
    }
  ],
  "related_topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
}

REQUIREMENTS:
- Generate 7-10 questions with varied difficulty
- Mix of easy (40%), medium (40%), hard (20%)
- All options must be plausible but clearly distinguishable
- Answer must exactly match one of the options
- Related topics should be real Wikipedia article names
```

## Local Development Setup

### Prerequisites
- Python 3.10 or higher
- Node.js 16 or higher
- MySQL database access
- Google Gemini API key

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "DATABASE_URL=your_mysql_url" >> .env

# Initialize database
python -c "from database import init_db; init_db()"

# Start server
python run.py
```

Backend will run on http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env.development

# Start development server
npm start
```

Frontend will run on http://localhost:3000

## Testing

### Manual Testing

1. Open https://ai-quiz-generator-pink.vercel.app
2. Enter a Wikipedia URL in the input field
3. Click "Generate Quiz" button
4. Wait 20-30 seconds for AI processing
5. View generated quiz with questions and details
6. Switch to "Quiz History" tab
7. Click "View Details" on any quiz
8. Try "Take Quiz" interactive mode

### Test URLs

Use these Wikipedia articles for comprehensive testing:
- https://en.wikipedia.org/wiki/Python_(programming_language)
- https://en.wikipedia.org/wiki/Artificial_intelligence
- https://en.wikipedia.org/wiki/Albert_Einstein
- https://en.wikipedia.org/wiki/World_War_II
- https://en.wikipedia.org/wiki/Climate_change

### API Testing with curl

```bash
# Test health endpoint
curl https://ai-quiz-generator-c20h.onrender.com/health

# Generate quiz
curl -X POST https://ai-quiz-generator-c20h.onrender.com/api/generate_quiz/ \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Python_(programming_language)","force":false}'

# Get history
curl https://ai-quiz-generator-c20h.onrender.com/api/history/

# Get specific quiz
curl https://ai-quiz-generator-c20h.onrender.com/api/quiz/1/
```

## Project Structure

```
ai-quiz-generator/
├── backend/
│   ├── database.py              # SQLAlchemy models and connection
│   ├── models.py                # Pydantic schemas
│   ├── config.py                # Configuration settings
│   ├── scraper.py               # Wikipedia scraping logic
│   ├── llm_quiz_generator.py   # AI quiz generation
│   ├── main.py                  # FastAPI application
│   ├── run.py                   # Server startup script
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables (not in git)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── QuizDisplay.jsx      # Quiz rendering component
│   │   │   ├── Modal.jsx            # Modal dialog component
│   │   │   ├── LoadingSpinner.jsx   # Loading state component
│   │   │   └── TakeQuizMode.jsx     # Interactive quiz component
│   │   ├── tabs/
│   │   │   ├── GenerateQuizTab.jsx  # Quiz generation tab
│   │   │   └── HistoryTab.jsx       # Quiz history tab
│   │   ├── services/
│   │   │   └── api.js               # API client
│   │   ├── App.js                   # Main application component
│   │   ├── index.js                 # React entry point
│   │   └── index.css                # Tailwind CSS styles
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.production              # Production environment vars
│
└── README.md                        # This file
```

## Performance Considerations

- Quiz generation takes 20-30 seconds on average
- Caching reduces response time for duplicate URLs to under 1 second
- Free tier Gemini API has rate limits (15 requests per minute)
- Database connection pooling handles concurrent requests
- Frontend uses loading states for better user experience
- Render free tier may have cold start delays (30-60 seconds for first request)

## Security Features

- Environment variables for sensitive data
- Input validation on all endpoints
- URL format validation for Wikipedia links
- CORS protection with allowed origins
- SQL injection prevention via SQLAlchemy ORM
- Content sanitization before processing
- Error messages don't expose internal details

## Known Limitations

- Free tier Render deployment has cold starts after inactivity
- Gemini API rate limits on free tier (15 requests/minute)
- Railway MySQL free tier limited to 500MB storage
- Very long Wikipedia articles (>15,000 chars) are truncated
- Quiz generation time varies based on article length

## Troubleshooting

### Backend Issues
- **Server cold start**: First request may take 30-60 seconds
- **Rate limit errors**: Wait 60 seconds between requests on free tier
- **Database connection errors**: Check Railway MySQL status

### Frontend Issues
- **CORS errors**: Verify backend CORS settings include your Vercel URL
- **API timeout**: Quiz generation can take up to 30 seconds
- **Blank page**: Check browser console for JavaScript errors

## Future Improvements

- Add Redis caching for faster response times
- Implement user authentication and quiz management
- Add quiz sharing functionality
- Support for multiple languages
- Question difficulty analysis
- Export quiz to PDF functionality
- Quiz analytics dashboard

## License

This project was developed as part of the DeepKlarity Technologies technical assessment.

## Contact

For questions or issues, please contact the developer.

## Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI framework for backend development
- React and Tailwind CSS for frontend
- Render for backend hosting
- Vercel for frontend hosting
- Railway for database hosting
- Wikipedia for content source

***
