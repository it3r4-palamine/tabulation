from django import forms
from ..models.multiple_choice import *


class Choice_form(forms.ModelForm):
	class Meta:
		model  = Choice
		fields = ('value','question','is_active','is_answer','is_import','is_related_required')