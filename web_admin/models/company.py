from ..models.transaction_types import *
from django.contrib.postgres.fields import ArrayField
from utils.dict_types import *


class Company(models.Model):
	name             = models.CharField(max_length=200,blank=True,null=True)
	is_active        = models.BooleanField(default=1)
	is_intelex       = models.BooleanField(default=0)

	class Meta:
		app_label = "web_admin"
		db_table  = "company"

	def __str__(self):
		return self.name

	def get_dict(self):
		return {
			"id" 		: self.pk,
			"name" 		: self.name,
			"is_active" : self.is_active
		}


class Company_rename(models.Model):
	name             = models.CharField(max_length=200,blank=True,null=True)
	is_active        = models.BooleanField(default=1)
	transaction_type = ArrayField(models.IntegerField("Transaction_type"),blank=True,null=True)
	company 		 = models.ForeignKey("Company",blank=True,null=True, on_delete=models.CASCADE)
	is_intelex		 = models.BooleanField(default=0)
	program_id		 = models.IntegerField(blank=True,null=True)
	rate 			 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=8)
	hours 			 = models.DurationField(blank=True, null=True)

	class Meta:
		app_label = "web_admin"
		db_table  = "company_rename"


	def get_dict(self,dict_type = DEFAULT):

		instance = {}

		if dict_type == DEFAULT:
			return {
				"id" 		 		: self.pk,
				"name" 		 		: self.name,
				"is_active"  		: self.is_active,
				"program_id" 		: self.program_id,
				"is_intelex" 		: self.is_intelex,
				"transaction_type" 	: self.transaction_type,
				"company" 	 		: self.company.pk,
				"rate"				: self.rate,
				"hours"				: self.hours.total_seconds() if self.hours else 0,
			}

		if dict_type == DEVICE:
			instance["id"] = self.pk
			instance["name"] = self.name
			instance["rate"] = self.rate
			instance["hours"] = self.hours.total_seconds() if self.hours else 0

			return instance


		if dict_type == FOR_LABEL:
			instance['name'] = self.name
			return instance

		if dict_type == UI_SELECT:
			instance['id'] = self.id
			instance['name'] = self.name
			return instance

		else:

			instance['id'] = self.id
			instance['name'] = self.name
			instance["hours"] = self.hours.total_seconds() if self.hours else 0
			instance['rate'] = convert_decimal_single(self.rate)
			instance['exercise_count'] = self.get_exercise_count()

			return instance


		