from django.db import models

class Transaction_type(models.Model):
	name      = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	company	  = models.ForeignKey("Company",blank=True,null=True)


	class Meta:
		app_label = "systech_account"
		db_table  = "transaction_types"


	def get_dict(self):
		return {
			"id" : self.pk,
			"name" : self.name,
			"is_active" : self.is_active,
		}
