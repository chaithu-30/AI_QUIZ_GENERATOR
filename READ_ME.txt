# AI Wiki Quiz Generator - README

## Project Overview

This is a full-stack application that generates AI-powered quizzes from Wikipedia articles using Google Gemini and FastAPI. The system scrapes Wikipedia content, processes it with a Large Language Model, and presents interactive quizzes to users.

## Technical Stack

**Backend:**
- Python 3.13
- FastAPI web framework
- SQLAlchemy ORM
- Railway MySQL database
- Google Generative AI (Gemini 2.5 Flash)
- BeautifulSoup4 for web scraping
- Pydantic for data validation

**Frontend:**
- React 18
- Tailwind CSS
- Axios for HTTP requests

## Features

### Core Functionality
- Generate quizzes from any Wikipedia article URL
- Automatic extraction of article content and entities
- AI-generated questions with multiple choice options
- Difficulty levels (easy, medium, hard)
- Explanations for each answer
- Related topics suggestions
- Quiz history with persistent storage
- Caching to prevent duplicate processing

### Bonus Features
- URL validation
- Interactive "Take Quiz" mode with scoring
- Raw HTML storage in database
- Responsive design
- Loading states and error handling

## Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- MySQL database (Railway or local)
- Google Gemini API key

## Installation Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with your credentials:
```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=mysql+pymysql://user:password@host:port/database
```

5. Initialize the database:
```bash
python -c "from database import init_db; init_db()"
```

6. Start the backend server:
```bash
python run.py
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create a .env file:
```
REACT_APP_API_URL=http://localhost:8000/api
```

4. Start the development server:
```bash
npm start
```

The application will open at http://localhost:3000

## Project Structure

```
ai-quiz-generator/
├── backend/
│   ├── venv/
│   ├── database.py              # Database models and connection
│   ├── models.py                # Pydantic schemas for validation
│   ├── config.py                # Application configuration
│   ├── scraper.py               # Wikipedia scraping logic
│   ├── llm_quiz_generator.py   # AI quiz generation
│   ├── main.py                  # FastAPI application and endpoints
│   ├── run.py                   # Server startup script
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── QuizDisplay.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── TakeQuizMode.jsx
│   │   ├── tabs/
│   │   │   ├── GenerateQuizTab.jsx
│   │   │   └── HistoryTab.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
│
├── sample_data/
│   ├── test_urls.txt
│   └── sample_outputs/
│
├── screenshots/
│
└── README.md
```

## API Documentation

### Endpoints

**POST /api/generate_quiz/**

Generate a new quiz from a Wikipedia URL.

Request body:
```json
{
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "force": false
}
```

Response:
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "title": "Python (programming language)",
  "summary": "Brief article summary...",
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
  "related_topics": ["Programming language", "Software development"],
  "cached": false
}
```

**GET /api/history/**

Retrieve a list of all generated quizzes.

Response:
```json
[
  {
    "id": 1,
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "title": "Python (programming language)",
    "date_generated": "2025-11-15T16:00:16"
  }
]
```

**GET /api/quiz/{quiz_id}/**

Get details of a specific quiz by ID.

Response:
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "date_generated": "2025-11-15T16:00:16",
  "full_quiz_data": {
    "title": "Python (programming language)",
    "summary": "...",
    "quiz": [...],
    ...
  }
}
```

**GET /health**

Check API health status.

**GET /docs**

Interactive API documentation (Swagger UI).

## Database Schema

### Quiz Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| url | String(500) | Wikipedia article URL (unique) |
| title | String(255) | Article title |
| date_generated | DateTime | Quiz creation timestamp |
| scraped_content | Text | Raw HTML content (optional) |
| full_quiz_data | Text | JSON-serialized quiz data |

## LLM Prompt Template

The system uses a structured prompt to ensure high-quality quiz generation:

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
- 7-10 multiple choice questions
- Extract key entities (people, organizations, locations)
- Identify main article sections
- Write a concise 2-3 sentence summary
- Suggest 5 related Wikipedia topics

REQUIREMENTS:
- Mix of easy (40%), medium (40%), hard (20%)
- All options must be plausible but clearly distinguishable
- Answer must exactly match one of the options
- Related topics should be real Wikipedia article names
```

## Testing

### Manual Testing

1. Start both backend and frontend servers
2. Open http://localhost:3000 in your browser
3. Enter a Wikipedia URL in the input field
4. Click "Generate Quiz" button
5. View the generated quiz with questions and details
6. Switch to "Quiz History" tab
7. Click "View Details" on any quiz
8. Try the "Take Quiz" interactive mode

### Test URLs

Use these Wikipedia articles for testing:
- https://en.wikipedia.org/wiki/Python_(programming_language)
- https://en.wikipedia.org/wiki/Artificial_intelligence
- https://en.wikipedia.org/wiki/Albert_Einstein
- https://en.wikipedia.org/wiki/World_War_II
- https://en.wikipedia.org/wiki/Climate_change

### API Testing

Using curl:
```bash
# Generate quiz
curl -X POST http://localhost:8000/api/generate_quiz/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"}'

# Get history
curl http://localhost:8000/api/history/

# Get specific quiz
curl http://localhost:8000/api/quiz/1/
```

## Troubleshooting

### Backend Issues

**Server won't start:**
- Verify virtual environment is activated
- Check .env file has correct API keys
- Ensure Railway database is accessible
- Check port 8000 is not already in use

**Quiz generation fails:**
- Verify Gemini API key is valid
- Check API quota (15 requests per minute on free tier)
- Ensure Wikipedia URL format is correct
- Check network connectivity

**Database errors:**
- Verify DATABASE_URL format in .env
- Check Railway database credentials
- Ensure database tables are initialized

### Frontend Issues

**Application won't load:**
- Verify backend is running on port 8000
- Check REACT_APP_API_URL in .env
- Clear browser cache and reload
- Check console for JavaScript errors

**CORS errors:**
- Verify CORS middleware is configured in main.py
- Check allowed origins include localhost:3000
- Restart both frontend and backend servers

## Deployment

### Backend Deployment (Railway/Render)

1. Create a new project on Railway or Render
2. Connect your GitHub repository
3. Set environment variables (GEMINI_API_KEY, DATABASE_URL)
4. Deploy from main branch
5. Note the deployed API URL

### Frontend Deployment (Vercel/Netlify)

1. Build the production version:
```bash
npm run build
```

2. Deploy to Vercel or Netlify
3. Set REACT_APP_API_URL to your deployed backend URL
4. Deploy from build folder

## Performance Considerations

- Quiz generation takes 20-30 seconds on average
- Caching reduces load time for duplicate URLs
- Free tier Gemini API has rate limits (15 requests/minute)
- Database connection pooling handles concurrent requests
- Frontend uses loading states for better user experience

## Security Notes

- Never commit .env files to version control
- Rotate API keys regularly
- Use environment variables for all sensitive data
- Validate all user inputs on backend
- Sanitize Wikipedia content before processing
- Use HTTPS in production

## License

This project was developed as part of the DeepKlarity Technologies technical assessment.

## Author

Full Stack Developer
Contact: your.email@example.com

## Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI framework for backend
- React and Tailwind CSS for frontend
- Railway for database hosting
- Wikipedia for content source