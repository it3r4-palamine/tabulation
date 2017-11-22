from django import forms
from ..models.settings import *


class Display_setting_form(forms.ModelForm):
	class Meta:
		model  = Display_setting
		fields = ('company_assessments','transaction_types','questions','company')