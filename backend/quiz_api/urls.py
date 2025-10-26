from django.urls import path
from .views import GenerateQuizView, HistoryView, QuizDetailView

urlpatterns = [
    path('generate_quiz/', GenerateQuizView.as_view(), name='generate_quiz'),
    path('history/', HistoryView.as_view(), name='history'),
    path('quiz/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz_detail'),
]
