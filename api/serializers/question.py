from rest_framework import serializers
from web_admin.models.question import Question, QuestionChoices


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('name',
                  'subject',
                  'question_type',
                  'company',
                  )


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoices
        fields = ('name',
                  'is_correct',
                  'question',
                  )
