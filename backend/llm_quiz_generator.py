"""
Quiz generator using Google's native Generative AI SDK
"""
import google.generativeai as genai
from models import QuizOutput
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

def get_llm():
    """Get Gemini model instance"""
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    # Use the working Gemini 2.5 Flash model
    return genai.GenerativeModel(
        model_name='models/gemini-2.5-flash',  # ✓ This works!
        generation_config=generation_config
    )

QUIZ_GENERATION_PROMPT = """You are an expert educational content creator. Generate a comprehensive quiz based STRICTLY on the Wikipedia article provided.

**STRICT RULES:**
- Use ONLY information from the article text below
- DO NOT use external knowledge
- Every question must be answerable from the article
- Include section references in explanations
- Ensure diverse difficulty levels (easy, medium, hard)

**ARTICLE TITLE:** {title}

**ARTICLE TEXT:**
{article_text}

**YOUR TASK:**
Generate a quiz with the following structure in pure JSON format (no markdown):

{{
  "title": "Article Title",
  "summary": "Brief 2-3 sentence summary of the article",
  "key_entities": {{
    "people": ["Person 1", "Person 2"],
    "organizations": ["Organization 1", "Organization 2"],
    "locations": ["Location 1", "Location 2"]
  }},
  "sections": ["Section 1", "Section 2", "Section 3"],
  "quiz": [
    {{
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option exactly as written in options",
      "difficulty": "easy",
      "explanation": "Brief explanation with reference to article section"
    }}
  ],
  "related_topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
}}

**REQUIREMENTS:**
- Generate 7-10 questions with varied difficulty
- Mix of easy (40%), medium (40%), hard (20%)
- All options must be plausible but clearly distinguishable
- Answer must exactly match one of the options
- Related topics should be real Wikipedia article names

Generate ONLY the JSON output, no additional text:"""

def clean_json_response(text: str) -> str:
    """Remove markdown formatting from response"""
    text = text.strip()
    
    # Remove markdown code blocks if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]  # Remove first line
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # Remove last line
        text = "\n".join(lines)
    
    return text.strip()

def generate_quiz_from_article(title: str, article_text: str, retry_count: int = 0) -> dict:
    """
    Generate quiz using Google's Generative AI SDK
    
    Args:
        title: Wikipedia article title
        article_text: Cleaned article content
        retry_count: Current retry attempt
        
    Returns:
        Dictionary containing validated quiz data
        
    Raises:
        Exception: If generation fails after retries
    """
    max_retries = 2
    
    try:
        # Get model
        model = get_llm()
        
        # Truncate article if too long (avoid token limits)
        max_length = 15000
        if len(article_text) > max_length:
            article_text = article_text[:max_length] + "\n\n[Article truncated for processing]"
        
        # Format prompt
        prompt = QUIZ_GENERATION_PROMPT.format(
            title=title,
            article_text=article_text
        )
        
        print(f"🤖 Generating quiz for: {title} (Attempt {retry_count + 1})")
        start_time = time.time()
        
        # Generate content
        response = model.generate_content(prompt)
        
        elapsed = time.time() - start_time
        print(f"✓ LLM responded in {elapsed:.2f} seconds")
        
        # Extract and clean response text
        response_text = response.text
        clean_text = clean_json_response(response_text)
        
        # Parse JSON
        try:
            quiz_data = json.loads(clean_text)
        except json.JSONDecodeError as je:
            print(f"✗ JSON parsing error: {je}")
            print(f"Response preview: {clean_text[:300]}...")
            raise Exception(f"Invalid JSON from LLM: {je}")
        
        # Validate with Pydantic schema
        validated = QuizOutput(**quiz_data)
        
        print(f"✓ Quiz validated: {len(validated.quiz)} questions")
        
        return validated.model_dump()
        
    except Exception as e:
        error_msg = str(e)
        print(f"✗ Attempt {retry_count + 1} failed: {error_msg[:200]}")
        
        # Handle quota errors
        if "429" in error_msg or "quota" in error_msg.lower() or "RESOURCE_EXHAUSTED" in error_msg:
            raise Exception(
                "Gemini API quota exceeded. Free tier: 60 requests/minute for gemini-pro. "
                "Wait 60 seconds or get new API key at https://aistudio.google.com/apikey"
            )
        
        # Retry on transient errors
        if retry_count < max_retries:
            if any(term in error_msg.lower() for term in ["timeout", "500", "503", "temporarily"]):
                wait_time = (retry_count + 1) * 5
                print(f"⏳ Retrying in {wait_time}s...")
                time.sleep(wait_time)
                return generate_quiz_from_article(title, article_text, retry_count + 1)
        
        # Final failure
        raise Exception(f"Quiz generation failed: {error_msg}")
