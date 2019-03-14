from rest_framework import serializers
from web_admin.models.exercise import ExerciseQuestion


class ExerciseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseQuestion
        fields = ('question',
                  'exercise',
                  )