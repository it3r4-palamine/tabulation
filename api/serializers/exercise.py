from rest_framework import serializers
from web_admin.models.exercise import Exercise, ExerciseQuestion


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = (
            'name',
            'transaction_code',
            'is_post_test',
            'is_assessment_test',
            'course',
            'company',
        )


class ExerciseQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseQuestion
        fields = ('question',
                  'exercise',
                  )