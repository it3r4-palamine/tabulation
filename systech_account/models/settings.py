from django.db import models

class Display_setting(models.Model):
	company_assessments = models.CharField(max_length=200,blank=True,null=True)
	transaction_types 	= models.CharField(max_length=200,blank=True,null=True)
	questions 			= models.CharField(max_length=200,blank=True,null=True)
	company 			= models.ForeignKey("Company")

	class Meta:
		app_label = "systech_account"
		db_table  = "display_settings"


	def get_dict(self):
		return {
			"id" : self.pk,
			"company_assessments" : self.company_assessments,
			"transaction_types" : self.transaction_types,
			"questions" : self.questions,
		}
