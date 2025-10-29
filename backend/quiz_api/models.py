from django.db import models
from django.utils import timezone

class Quiz(models.Model):
    url = models.URLField(max_length=500, unique=True, db_index=True)
    title = models.CharField(max_length=500)
    date_generated = models.DateTimeField(auto_now_add=True)
    scraped_html = models.TextField(blank=True, null=True, 
                                    help_text="Raw HTML from Wikipedia")
    cleaned_text = models.TextField(help_text="Cleaned article text for LLM")
    
    # Store complete quiz JSON as text
    full_quiz_data = models.TextField(
        help_text="Complete quiz JSON including questions, entities, and related topics"
    )
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ['-date_generated']  # Most recent first
        
    def __str__(self):
        return f"{self.title} - {self.date_generated.strftime('%Y-%m-%d')}"
