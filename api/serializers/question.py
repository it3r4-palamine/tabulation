from rest_framework import serializers
from systech_account.models.question import Question, QuestionChoices


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('name',
                  'subject',
                  'question_type',
                  )


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoices
        fields = ('name',
                  'is_correct',
                  'question',
                  )
