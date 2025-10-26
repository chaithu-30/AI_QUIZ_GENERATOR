from rest_framework import serializers
from .models import Quiz
import json

class QuizSerializer(serializers.ModelSerializer):
    """Serializer for the Quiz model"""
    
    # Parse full_quiz_data JSON when returning data
    full_quiz_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'url', 'title', 'date_generated', 'full_quiz_data']
        read_only_fields = ['id', 'date_generated']
    
    def get_full_quiz_data(self, obj):
        """Parse the JSON string into a Python dict"""
        if obj.full_quiz_data:
            return json.loads(obj.full_quiz_data)
        return None


class QuizListSerializer(serializers.ModelSerializer):
    """Simplified serializer for history list"""
    
    class Meta:
        model = Quiz
        fields = ['id', 'url', 'title', 'date_generated']
        read_only_fields = ['id', 'date_generated']
