from django import forms
from ..models.transaction_types import *


class Transaction_type_form(forms.ModelForm):
	class Meta:
		model  = Transaction_type
		fields = ('name','is_active','company')