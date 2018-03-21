from django.db import models

class Choice(models.Model):
	value            		= models.CharField(max_length=200,blank=True,null=True)
	is_active        		= models.BooleanField(default=1)
	question         		= models.ForeignKey("Assessment_question")
	is_answer   	 		= models.BooleanField(default=0)
	is_import   	 		= models.BooleanField(default=0)
	follow_up_required  	= models.BooleanField(default=0)
	required_document_image = models.BooleanField(default=0)
	company 				= models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "choices"

	def get_dict(self):
		return {
			"id" 					  : self.pk,
			"value" 				  : self.value,
			"question" 				  : self.question.get_dict(),
			"is_answer" 			  : self.is_answer,
			"is_active" 			  : self.is_active,
			"is_import" 			  : self.is_import,
			"follow_up_required" 	  : self.follow_up_required,
			"required_document_image" : self.required_document_image,
		}