from django import forms
from ..models.timeslot import TimeSlot

class TimeSlotForm(forms.ModelForm):
	class Meta:
		model = TimeSlot
		fields = ('student', 
				  'time_start', 
				  'time_end', 
				  'has_monday',
				  'has_tuesday', 
				  'has_wednesday', 
				  'has_thursday', 
				  'has_friday', 
				  'has_saturday', 
				  'is_current')
