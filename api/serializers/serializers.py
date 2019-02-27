from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from web_admin.models.assessments import *
from web_admin.models.user import *


class AnswerSerializer(serializers.ModelSerializer):
	# document_image = Base64ImageField(required=False)

	class Meta:
		model = Assessment_answer
		fields = ('id', 'question', 'company_assessment', 'choice', 'text_answer', 'document_image', 'transaction_type', 'uploaded_question')

class AnswerImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Assessment_answer_image
		fields = ('id', 'question', 'company_assessment', 'transaction_type', 'image', 'item_no', 'is_active')

class AnswerImageIOSSerializer(serializers.ModelSerializer):
	image = Base64ImageField(required=False)

	class Meta:
		model = Assessment_answer_image
		fields = ('id', 'question', 'company_assessment', 'transaction_type', 'image', 'item_no', 'is_active')


class LessonUpdateHeaderSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Lesson_update_header
		fields = ('id', 'user', 'date')


class LessonUpdateDetailSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Lesson_update_detail
		fields = ('id', 'lesson_update_header', 'lesson', 'to_dos_topic')