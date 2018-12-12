from django.db import models
from django.core.validators import RegexValidator

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

class School(models.Model):
	name 			= models.CharField(max_length=100, blank=False, null=False)
	address 		= models.TextField(blank=False, null=False)
	contact_person 	= models.CharField(max_length=200, blank=True, null=True)
	phone_regex 	= RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	contact_number 	= models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True) # validators should be a list
	is_active 		= models.BooleanField(default=True)
	is_deleted 		= models.BooleanField(default=False)
	company    		= models.ForeignKey("Company",blank=True,null=True)

	class Meta:
	    app_label = "systech_account"
	    db_table  = "school"
	    ordering  = ["id"]

	def get_dict(self):

	    instance = {}
	    instance["id"] = self.id
	    instance["name"] = self.name
	    instance["is_active"] = self.is_active

	    return instance

class GradeLevel(models.Model):
    name 		= models.CharField(max_length=50, blank=False, null=False)
    is_active 	= models.BooleanField(default=True)
    is_deleted 	= models.BooleanField(default=False)
    company    	= models.ForeignKey("Company",blank=True,null=True)
     
    class Meta:
        app_label = "systech_account"
        db_table  = "grade_level"
        ordering  = ["id"]

    def get_dict(self):
		instance 		 = {}
		instance["id"] 	 = self.id
		instance["name"] = self.name
		instance["is_active"] = self.is_active

		return instance


class TrainerNote(models.Model):
	name = models.TextField()
	code = models.CharField(max_length=100, blank=True, null=True)
	score_min = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
	score_max = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
	is_active  = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)

	class Meta:
		app_label = "systech_account"
		db_table  = "trainer_note"
		ordering  = ["id"]

	def get_dict(self):

		instance = {}
		instance['id'] = self.id
		instance['name'] = self.name
		instance['score_min'] = self.score_min
		instance['score_max'] = self.score_max

		instance = obj_decimal_to_float(instance)

		return instance
