from django import forms
from ..models.crud import *


class Record_form(forms.ModelForm):
	class Meta:
		model = Record
		fields = ('name',)