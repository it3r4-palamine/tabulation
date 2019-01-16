from django import forms
from ..models.enrollment import *

class Enrollment_form(forms.ModelForm):
	class Meta:
		model = Enrollment
		fields = ('user', 
				  'company_rename',
				  'school', 
				  'code',
				  'timeslot',
				  'session_credits',
				  'session_start_date', 
				  'session_end_date', 
				  'enrollment_date',
				  'company')

class Enrollment_type_form(forms.ModelForm):
	class Meta:
		model = EnrollmentType
		fields = ('name', 
				  'code',
				  'company')
