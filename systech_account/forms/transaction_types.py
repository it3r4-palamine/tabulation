from django import forms
from ..models.transaction_types import *
from django.db.models import Q

class Transaction_type_form(forms.ModelForm):
	class Meta:
		model  = Transaction_type
		fields = ('name','transaction_code','is_active','company','exercise_id','set_no','total_items','is_intelex')


	def clean(self,):
		raw_data = self.cleaned_data

		transaction_code = (Q(transaction_code = raw_data["transaction_code"]) & Q(is_active = True))

		instance = Transaction_type.objects.filter(transaction_code)
		if instance.exists():
			instance = instance.first()
			if instance.pk != self.instance.pk and raw_data["transaction_code"]:
				if not raw_data['is_intelex']:
					raise ValueError(raw_data["transaction_code"] + " transaction code already exist.")

		return raw_data