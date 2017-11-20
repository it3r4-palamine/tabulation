from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from systech_account.models.assessments import *


class AnswerSerializer(serializers.ModelSerializer):
	document_image = Base64ImageField(required=False)

	class Meta:
		model = Assessment_answer
		fields = ('id', 'question', 'company_assessment', 'choice', 'text_answer', 'document_image', 'transaction_type')