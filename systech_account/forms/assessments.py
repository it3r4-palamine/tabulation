from django import forms
from ..models.assessments import *


class Assessment_question_form(forms.ModelForm):
	class Meta:
		model  = Assessment_question
		fields = (
			'value',
			'is_active',
			'transaction_type',
			'is_multiple',
			'parent_question',
			'is_document',
			'code',
			'is_import',
			'has_multiple_answer',
			'is_general',
			'transaction_types',
			'has_follow_up',
			'company',
			'answer_type',
			'has_related',
			'uploaded_question',
			'timer',
		)

class Assessment_effect_form(forms.ModelForm):
	class Meta:
		model  = Assessment_effect
		fields = ('value','is_active','question','is_import','company')

class Assessment_recommendation_form(forms.ModelForm):
	class Meta:
		model  = Assessment_recommendation
		fields = ('value','is_active','is_import','company')

class Assessment_finding_form(forms.ModelForm):
	class Meta:
		model  = Assessment_finding
		fields = ('value','is_active','question','is_import','company')

class Generated_assessment_recommendation_form(forms.ModelForm):
	class Meta:
		model  = Generated_assessment_recommendation
		fields = ('recommendations','company_assessment','company')

class Related_question_form(forms.ModelForm):
	class Meta:
		model  = Related_question
		fields = ('related_questions','is_active','is_import','company')

class Assessment_score_form(forms.ModelForm):
	class Meta:
		model  = Assessment_score
		fields = ('transaction_type','is_active','company_assessment','score','question','uploaded_question') 

class Assessment_session_form(forms.ModelForm):
	class Meta:
		model  = Assessment_session
		fields = ('company_assessment','date','time_start','time_end','is_deleted','transaction_type','question')

class Assessment_image_form(forms.ModelForm):
	class Meta:
		model  = Assessment_image
		fields = ('company','is_active','image','question')

class Assessment_image_answer_form(forms.ModelForm):
	class Meta:
		model  = Assessment_image_answer
		fields = ('company','is_active','question','answer','item_no')

class Assessment_upload_answer_form(forms.ModelForm):
	class Meta:
		model  = Assessment_upload_answer
		fields = ('question','is_active','is_deleted','answer','item_no','company_assessment','transaction_type')

class Multiple_image_answer_form(forms.ModelForm):
	class Meta:
		model  = Multiple_image_answer
		fields = ('image_answer','is_active','name')