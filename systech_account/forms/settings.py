from django import forms
from ..models.settings import *


class Display_setting_form(forms.ModelForm):
	class Meta:
		model  = Display_setting
		fields = ('company_assessments','transaction_types','questions','company','company_rename')

class Math_symbol_form(forms.ModelForm):
	class Meta:
		model  = Math_symbol
		fields = ('symbol','name','is_active','company','category')