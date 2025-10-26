# AI Wiki Quiz Generator

Generate AI-powered quizzes from Wikipedia articles using Django, React, MySQL, and Google Gemini.

## Features

-  AI-powered quiz generation using Google Gemini 2.5 Flash via LangChain
- Automatic Wikipedia article scraping with BeautifulSoup
- MySQL database storage for quiz history
- Clean React UI with two tabs (Generate & History)
-  Structured output with questions, entities, and related topics
- Duplicate URL detection and caching

## Tech Stack

**Backend:**
- Python 3.13
- Django 5.1 + Django REST Framework
- MySQL
- LangChain + Google Gemini API
- BeautifulSoup4

**Frontend:**
- React 18 (Create React App)
- Axios for API calls
- Custom CSS styling

## Project Structure

ai-quiz-generator/
├── backend/
│ ├── quiz_project/ # Django project settings
│ ├── quiz_api/ # Main API app
│ │ ├── models.py # Quiz database model
│ │ ├── views.py # API endpoints
│ │ ├── serializers.py # DRF serializers
│ │ ├── schemas.py # Pydantic schemas for LLM
│ │ ├── scraper.py # Wikipedia scraping logic
│ │ ├── llm_quiz_generator.py # LangChain integration
│ │ └── urls.py # API routing
│ ├── manage.py
│ ├── requirements.txt
│ └── .env # API keys (not committed)
└── frontend/
├── src/
│ ├── components/ # React components
│ ├── services/api.js # API service layer
│ └── App.js
└── package.json

text

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 16+
- MySQL 8.0+
- Google Gemini API key ([Get it here](https://aistudio.google.com/api-keys?_gl=1*16wvpxc*_ga*MTM5Mjg3MzQ4My4xNzYxNDU4NjUz*_ga_P1DBVKWT6V*czE3NjE0ODg3ODUkbzIkZzAkdDE3NjE0ODg3ODUkajYwJGwwJGgxNTI5MjkyODg2

### Backend Setup

1. **Navigate to backend folder:**
cd backend

text

2. **Create virtual environment:**
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # Mac/Linux

text

3. **Install dependencies:**
pip install -r requirements.txt

text

4. **Create `.env` file:**
GEMINI_API_KEY=your_gemini_api_key_here
MYSQL_PASSWORD=your_mysql_password

text

5. **Create MySQL database:**
CREATE DATABASE quiz_generator_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

text

6. **Update `quiz_project/settings.py` with your MySQL credentials**

7. **Run migrations:**
python manage.py migrate

text

8. **Start Django server:**
python manage.py runserver

text
Backend will run at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend folder:**
cd frontend

text

2. **Install dependencies:**
npm install

text

3. **Start React app:**
npm start

text
Frontend will open at `http://localhost:3000`

## API Endpoints

### 1. Generate Quiz
**POST** `/api/generate_quiz/`

**Request:**
{
"url": "https://en.wikipedia.org/wiki/Alan_Turing",
"force": false
}

text

**Response:** Full quiz JSON with questions, entities, and related topics

### 2. Get History
**GET** `/api/history/`

**Response:** List of all quizzes (id, url, title, date_generated)

### 3. Get Quiz Details
**GET** `/api/quiz/<id>/`

**Response:** Full quiz data for specific quiz ID

## LangChain Prompt Template

The prompt used for quiz generation (from `llm_quiz_generator.py`):

"""You are an expert quiz generator. Your task is to create an educational quiz
based STRICTLY on the provided Wikipedia article text.

CRITICAL RULES:

Use ONLY information present in the article text below

Do NOT use external knowledge or make up facts

Generate exactly 5-10 questions with varied difficulty (easy, medium, hard)

Each question must have exactly 4 distinct options (A-D) with only ONE correct answer

Explanations should reference specific sections from the article when possible

Related topics must be actual Wikipedia-worthy topics related to the article subject

Article Title: {title}
Article Content: {content}

{format_instructions}

Generate the quiz now following the exact JSON schema provided above."""

text

The prompt uses LangChain's `JsonOutputParser` with a Pydantic schema to enforce:
- Exact field structure
- 5-10 questions
- Exactly 4 options per question
- Difficulty levels: easy/medium/hard only
- Key entities grouped by people/organizations/locations

## Testing

### Test Generate Quiz:
curl -X POST http://127.0.0.1:8000/api/generate_quiz/
-H "Content-Type: application/json"
-d @test_request.json

text

Where `test_request.json` contains:
{
"url": "https://en.wikipedia.org/wiki/Alan_Turing"
}

text

### Test History:
curl http://127.0.0.1:8000/api/history/

text

### Test Quiz Details:
curl http://127.0.0.1:8000/api/quiz/1/

text

## Sample Output

See `sample_data/` folder for example Wikipedia URLs and their generated quiz outputs.

## Features Implemented
All core requirements  
 Duplicate URL caching  
 Raw HTML storage  
 Error handling for invalid URLs  
Loading states and error messages  
 Modal for quiz details  
Responsive card-based layout  

## Known Limitations

- Rate limited by Gemini free tier (15 requests/minute)
- Very long articles are truncated to 15,000 characters
- Only English Wikipedia supported

## License

MIT
