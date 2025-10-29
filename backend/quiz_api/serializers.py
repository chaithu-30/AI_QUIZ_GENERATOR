from rest_framework import serializers
from .models import Quiz
import json

class QuizSerializer(serializers.ModelSerializer):
    full_quiz_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'url', 'title', 'date_generated', 'full_quiz_data']
        read_only_fields = ['id', 'date_generated']
    
    def get_full_quiz_data(self, obj):
        if obj.full_quiz_data:
            return json.loads(obj.full_quiz_data)
        return None


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'url', 'title', 'date_generated']
        read_only_fields = ['id', 'date_generated']
