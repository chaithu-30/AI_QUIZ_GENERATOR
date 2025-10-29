import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .schemas import QuizOutput

# Load environment variables from .env file
# Get the backend directory path (parent of quiz_api)
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / '.env'

# Load with verbose to debug
load_dotenv(dotenv_path, verbose=True)

# Verify it loaded
if not os.getenv('GEMINI_API_KEY'):
    print(f"Looking for .env at: {dotenv_path}")
    print(f".env file exists: {dotenv_path.exists()}")
    raise ValueError("GEMINI_API_KEY not found in environment variables")
def generate_quiz(title: str, cleaned_text: str) -> dict:
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    # Initialize Gemini model via LangChain
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=api_key,
    temperature=0.3,
    max_output_tokens=4096,
)
    parser = JsonOutputParser(pydantic_object=QuizOutput)
    
    # Get format instructions from the parser
    format_instructions = parser.get_format_instructions()
    
    # Create prompt template with strict instructions
    prompt_template = PromptTemplate(
        template="""You are an expert quiz generator. Your task is to create an educational quiz based STRICTLY on the provided Wikipedia article text.

**CRITICAL RULES:**
1. Use ONLY information present in the article text below
2. Do NOT use external knowledge or make up facts
3. Generate exactly 5-10 questions with varied difficulty (easy, medium, hard)
4. Each question must have exactly 4 distinct options (A-D) with only ONE correct answer
5. Explanations should reference specific sections from the article when possible
6. Related topics must be actual Wikipedia-worthy topics related to the article subject

**Article Title:** {title}

**Article Content:**
{content}

{format_instructions}

Generate the quiz now following the exact JSON schema provided above.""",
        input_variables=["title", "content"],
        partial_variables={"format_instructions": format_instructions}
    )
    
    # Create the LangChain chain: Prompt -> LLM -> Parser
    chain = prompt_template | llm | parser
    
    try:
        # Invoke the chain with article data
        result = chain.invoke({
            "title": title,
            "content": cleaned_text
        })
        
        # Validate that we got the expected structure
        if not isinstance(result, dict):
            raise ValueError("LLM did not return a valid dictionary")
        
        # Ensure required fields are present
        required_fields = ['title', 'summary', 'key_entities', 'sections', 'quiz', 'related_topics']
        missing_fields = [field for field in required_fields if field not in result]
        if missing_fields:
            raise ValueError(f"Missing required fields in LLM output: {missing_fields}")
        
        return result
        
    except Exception as e:
        # If parsing fails, try once more with stricter instructions
        print(f"First attempt failed: {e}. Retrying with stricter prompt...")
        
        retry_prompt = PromptTemplate(
            template="""IMPORTANT: You MUST return valid JSON matching this exact schema.

{format_instructions}

Article Title: {title}
Article Content (first 8000 chars): {content}

Generate a quiz with 5-7 questions only. Keep all text concise.""",
            input_variables=["title", "content"],
            partial_variables={"format_instructions": format_instructions}
        )
        
        retry_chain = retry_prompt | llm | parser
        
        try:
            # Truncate content for retry (reduce complexity)
            truncated_content = cleaned_text[:8000]
            result = retry_chain.invoke({
                "title": title,
                "content": truncated_content
            })
            return result
        except Exception as retry_error:
            raise Exception(f"Quiz generation failed after retry: {str(retry_error)}")
