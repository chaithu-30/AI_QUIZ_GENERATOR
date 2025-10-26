from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import traceback

from .models import Quiz
from .serializers import QuizSerializer, QuizListSerializer
from .scraper import scrape_wikipedia
from .llm_quiz_generator import generate_quiz

class GenerateQuizView(APIView):
    """
    POST /api/generate_quiz/
    Accepts a Wikipedia URL, scrapes content, generates quiz, and stores in DB
    """
    
    def post(self, request):
        url = request.data.get('url')
        
        if not url:
            return Response(
                {'error': 'URL is required in request body'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if quiz already exists
        existing_quiz = Quiz.objects.filter(url=url).first()
        if existing_quiz and not request.data.get('force', False):
            serializer = QuizSerializer(existing_quiz)
            # Return consistent structure with cache indicator
            return Response({
                **serializer.data,
                'cached': True,
                'message': 'Using cached quiz. Set force=true to regenerate.'
            }, status=status.HTTP_200_OK)
        
        try:
            # Step 1: Scrape Wikipedia
            scraped_data = scrape_wikipedia(url)
            title = scraped_data['title']
            cleaned_text = scraped_data['cleaned_text']
            raw_html = scraped_data['raw_html']
            
            # Step 2: Generate quiz with LLM
            quiz_data = generate_quiz(title, cleaned_text)
            
            # Step 3: Prepare complete response
            complete_data = {
                'url': url,
                'title': title,
                'summary': quiz_data.get('summary', ''),
                'key_entities': quiz_data.get('key_entities', {}),
                'sections': quiz_data.get('sections', []),
                'quiz': quiz_data.get('quiz', []),
                'related_topics': quiz_data.get('related_topics', [])
            }
            
            # Step 4: Store in database
            if existing_quiz:
                existing_quiz.title = title
                existing_quiz.cleaned_text = cleaned_text
                existing_quiz.scraped_html = raw_html
                existing_quiz.full_quiz_data = json.dumps(complete_data)
                existing_quiz.save()
                quiz_obj = existing_quiz
            else:
                quiz_obj = Quiz.objects.create(
                    url=url,
                    title=title,
                    cleaned_text=cleaned_text,
                    scraped_html=raw_html,
                    full_quiz_data=json.dumps(complete_data)
                )
            
            # Step 5: Return consistent structure
            serializer = QuizSerializer(quiz_obj)
            response_data = {
                **serializer.data,
                'cached': False,
                'message': 'Quiz generated successfully.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': f'Validation error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("Error generating quiz:")
            print(traceback.format_exc())
            return Response(
                {'error': f'Failed to generate quiz: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HistoryView(APIView):
    """
    GET /api/history/
    Returns list of all previously generated quizzes
    """
    
    def get(self, request):
        quizzes = Quiz.objects.all().order_by('-date_generated')
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizDetailView(APIView):
    """
    GET /api/quiz/<id>/
    Returns full details of a specific quiz by ID
    """
    
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)
