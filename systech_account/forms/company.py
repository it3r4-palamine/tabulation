from django import forms
from ..models.company import *


class Company_form(forms.ModelForm):
	class Meta:
		model  = Company
		fields = ('name','transaction_type','is_active')