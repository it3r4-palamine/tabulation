from django import forms
from ..models.subject import Subject

class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ('name',
				  'description', 
				  )
