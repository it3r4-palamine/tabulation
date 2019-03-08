from django import forms
from ..models.company import *


class CompanyForm(forms.ModelForm):
	class Meta:
		model  = Company
		fields = ('name',)


class Company_rename_form(forms.ModelForm):
	class Meta:
		model  = Company_rename
		fields = ('name','is_active','transaction_type','company','is_intelex','program_id','rate','hours')