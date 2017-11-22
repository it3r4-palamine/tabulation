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
			'is_related',
			'is_document',
			'code',
			'is_import',
			'has_multiple_answer',
			'is_general',
			'transaction_types',
			'has_follow_up',
			'company',	
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