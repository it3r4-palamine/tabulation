from django import forms
from ..models.session import *

class StudentSessionForm(forms.ModelForm):
	class Meta:
		model = StudentSession
		fields = ('student', 
				  'program', 
				  'enrollment', 
				  'code',
				  'session_date', 
				  'session_timein', 
				  'session_timeout', 
				  'comments')

		

class SessionExerciseForm(forms.ModelForm):
	class Meta:
		model = SessionExercise
		fields = ('session',
				  'exercise', 
				  'score', 
				  'trainer_note', 
				  'facilitated_by')
