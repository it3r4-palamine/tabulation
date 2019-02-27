from django.db import models

class Transaction_type(models.Model):
	name      		 = models.CharField(max_length=200,blank=True,null=True)
	transaction_code = models.CharField(max_length=200,blank=True,null=True)
	exercise_id 	 = models.IntegerField(blank=True, null=True)
	program_id  	 = models.IntegerField(blank=True, null=True)
	set_no 			 = models.IntegerField(blank=True, null=True)
	total_items 	 = models.IntegerField(blank=True, null=True)
	is_active 		 = models.BooleanField(default=1)
	is_intelex 		 = models.BooleanField(default=0)
	company	  		 = models.ForeignKey("Company",blank=True,null=True)


	class Meta:
		app_label = "web_admin"
		db_table  = "transaction_types"


	def get_dict(self, isV2=False):
		transaction_type = {}

		if isV2:
			transaction_type['transactionTypeId'] = self.pk
			transaction_type['transactionTypeName'] = self.name
		else:
			transaction_type['id'] = self.pk
			transaction_type['name'] = self.name
			transaction_type['transaction_code'] = self.transaction_code
			transaction_type['is_active'] = self.is_active
			transaction_type['exercise_id'] = self.exercise_id
			transaction_type['program_id'] = self.program_id
			transaction_type['set_no'] = self.set_no
			transaction_type['total_items'] = self.total_items
			transaction_type['is_intelex'] = self.is_intelex
			transaction_type['company'] = self.company.pk

		return transaction_type