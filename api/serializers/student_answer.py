from rest_framework import serializers
from web_admin.models.student_answer import StudentAnswer


class StudentAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentAnswer
        fields = ('student',
                  'exercise_question',
                  'question',
                  'answer',
                  )