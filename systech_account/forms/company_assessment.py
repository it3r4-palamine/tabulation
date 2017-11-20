from django import forms
from ..models.company_assessment import *


class Company_assessment_form(forms.ModelForm):
	class Meta:
		model  = Company_assessment
		fields = ('date_from','date_to','transaction_type','is_active','company','is_synced','is_complete','reference_no','consultant')