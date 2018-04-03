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
		app_label = "systech_account"
		db_table  = "transaction_types"


	def get_dict(self):
		return {
			"id" 			   : self.pk,
			"name" 			   : self.name,
			"transaction_code" : self.transaction_code,
			"is_active" 	   : self.is_active,
			"exercise_id" 	   : self.exercise_id,
			"program_id" 	   : self.program_id,
			"set_no" 		   : self.set_no,
			"total_items" 	   : self.total_items,
			"is_intelex" 	   : self.is_intelex,
		}
