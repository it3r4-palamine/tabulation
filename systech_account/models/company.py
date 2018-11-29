from django.db import models
from ..models.transaction_types import *
from django.contrib.postgres.fields import ArrayField

class Company(models.Model):
	name             = models.CharField(max_length=200,blank=True,null=True)
	is_active        = models.BooleanField(default=1)

	class Meta:
		app_label = "systech_account"
		db_table  = "company"


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
	company 		 = models.ForeignKey("Company",blank=True,null=True)
	is_intelex		 = models.BooleanField(default=0)
	program_id		 = models.IntegerField(blank=True,null=True)
	rate 			 = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=8)

	class Meta:
		app_label = "systech_account"
		db_table  = "company_rename"


	def get_dict(self):
		return {
			"id" 		 		: self.pk,
			"name" 		 		: self.name,
			"is_active"  		: self.is_active,
			"program_id" 		: self.program_id,
			"is_intelex" 		: self.is_intelex,
			"transaction_type" 	: self.transaction_type,
			"company" 	 		: self.company.pk,
			"rate"				: self.rate
		}