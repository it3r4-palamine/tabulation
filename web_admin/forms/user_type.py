from django import forms
from ..models.user import *
from django.db.models import Q

class User_type_form(forms.ModelForm):
	class Meta:
		model  = UserType
		fields = ('name','is_active','company','is_default')


	def clean(self,):
		raw_data = self.cleaned_data

		user_type = (Q(name = raw_data["name"]) & Q(is_active = True) & Q(company = raw_data["company"]))

		instance = UserType.objects.filter(user_type)
		if instance.exists():
			instance = instance.first()
			if instance.pk != self.instance.pk and raw_data["name"]:
				raise ValueError(raw_data["name"] + " already exist.")

		return raw_data