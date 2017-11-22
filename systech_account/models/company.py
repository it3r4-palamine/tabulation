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
			"id" : self.pk,
			"name" : self.name,
			# "transaction_type" : self.transaction_type.get_dict(),
			"is_active" : self.is_active
		}