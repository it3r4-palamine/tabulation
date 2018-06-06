from django.db import models

class Display_setting(models.Model):
	company_assessments = models.CharField(max_length=200,blank=True,null=True)
	transaction_types 	= models.CharField(max_length=200,blank=True,null=True)
	questions 			= models.CharField(max_length=200,blank=True,null=True)
	company_rename		= models.CharField(max_length=200,blank=True,null=True)
	company 			= models.ForeignKey("Company")

	class Meta:
		app_label = "systech_account"
		db_table  = "display_settings"


	def get_dict(self):
		return {
			"id" 				  : self.pk,
			"company_assessments" : self.company_assessments,
			"transaction_types"   : self.transaction_types,
			"questions" 		  : self.questions,
			"company_rename" 	  : self.company_rename,
		}

class Math_symbol(models.Model):
	symbol     = models.TextField(blank=True,null=True)
	name       = models.TextField(blank=True,null=True)
	company    = models.ForeignKey("Company")
	is_active  = models.BooleanField(default=1)
	category   = models.TextField(blank=True,null=True)
	above_text = models.BooleanField(default=0)
	syntax	   = models.TextField(blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "math_symbols"

	def get_dict(self):
		return {
			"id" 		 : self.pk,
			"symbol" 	 : self.symbol,
			"name" 		 : self.name,
			"is_active"  : self.is_active,
			"category" 	 : self.category,
			"above_text" : self.above_text,
			"syntax" 	 : self.syntax,
		}

class To_dos_topic(models.Model):
	name 	   = models.TextField(blank=True,null=True)
	company    = models.ForeignKey("Company")
	is_active  = models.BooleanField(default=1)

	class Meta:
		app_label = "systech_account"
		db_table  = "to_dos_topics"

	def get_dict(self):
		return {
			"id" 		: self.pk,
			"name" 		: self.name,
			"is_active" : self.is_active,
		}