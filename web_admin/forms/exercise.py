from django import forms
from ..models.exercise import *
from django.db.models import Q


class ExerciseForm(forms.ModelForm):

	class Meta:
		model  = Exercise
		fields = (
			'name',
			'transaction_code',
			'is_active',
			'company',
			'exercise_id',
			'set_no',
			'total_items',
			'is_intelex',
			'program_id')

	def clean(self,):
		raw_data = self.cleaned_data

		transaction_code = (Q(transaction_code = raw_data["transaction_code"]) & Q(is_active = True) & Q(company = raw_data["company"]) & Q(set_no = raw_data["set_no"]))

		instance = Exercise.objects.filter(transaction_code)
		if instance.exists():
			instance = instance.first()
			if instance.pk != self.instance.pk and raw_data["transaction_code"]:
				if not raw_data['is_intelex']:
					raise ValueError(raw_data["transaction_code"] + " transaction code already exist.")

		return raw_data