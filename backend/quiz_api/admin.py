from django.contrib import admin
from .models import Quiz

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'date_generated')
    list_filter = ('date_generated',)
    search_fields = ('title', 'url')
    readonly_fields = ('date_generated',)
