from django import forms
from ..models.user import *


class User_type_form(forms.ModelForm):
	class Meta:
		model  = User_type
		fields = ('name','is_active')