from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ..models.transaction_types import *
from ..models.company import *

import time

class User_Manager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')

		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password):
		if not email:
			raise ValueError('The given email must be set')

		user = self.model(email=email)
		user.set_password(password)
		user.is_admin = True
		user.save()
		return user

class User(AbstractBaseUser):
	email            = models.EmailField(max_length=100,unique=True,null=False,blank=False)
	fullname         = models.CharField(max_length=100,null=True,blank=True)
	is_admin         = models.BooleanField(default=False)
	is_active        = models.BooleanField(default=1)
	user_type        = models.ForeignKey("User_type",null=True,blank=True)
	is_edit          = models.BooleanField(default=False)
	company			 = models.ForeignKey("Company",blank=True,null=True)
	objects          = User_Manager()
	is_intelex       = models.BooleanField(default=False)
	user_intelex_id	 = models.IntegerField(blank=True,null=True)
	username 		 = models.CharField(max_length=100,unique=True,null=True,blank=True)

	USERNAME_FIELD = 'username'

	class Meta:
		app_label = "systech_account"
		db_table  = "User"

	def get_dict(self):
		return {
			"id" 	   : self.pk,
			"fullname" : self.fullname,
		}

	def delete(self):
		self.is_active = False
		self.email += ("__"+str(time.time()))

		self.save()

		return True

class User_type(models.Model):
	name       = models.CharField(max_length=200,blank=True,null=True)
	is_active  = models.BooleanField(default=1)
	is_default = models.BooleanField(default=0)
	company    = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "user_type"

	def get_dict(self):
		return {
			"id" 		 : self.pk,
			"name" 		 : self.name,
			"is_active"  : self.is_active,
			"is_default" : self.is_default
		}

class User_credit(models.Model):
	user 			   = models.ForeignKey("User")
	enrollment_id 	   = models.IntegerField(blank=True, null=True)
	session_credits    = models.DurationField(blank=True, null=True)
	session_start_date = models.DateField(blank=True, null=True)
	session_end_date   = models.DateField(blank=True, null=True)
	program_id	 	   = models.IntegerField(blank=True, null=True)
	program_name	   = models.CharField(max_length=200,blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "user_credits"

	def get_dict(self):
		return {
			'id' 				 : self.pk,
			'user' 				 : self.user.get_dict(),
			'enrollment_id' 	 : self.enrollment_id,
			'session_credits' 	 : self.session_credits.total_seconds(),
			'session_start_date' : self.session_start_date,
			'session_end_date'   : self.session_end_date,
			'program_id' 		 : self.program_id,
		}


class Lesson_update_header(models.Model):
	user 		 = models.ForeignKey("User")
	date 		 = models.DateField(blank=True, null=True)
	is_active 	 = models.BooleanField(default=1)


	class Meta:
		app_label = "systech_account"
		db_table  = "lesson_update_header"


	def get_dict(self):
		return {
			'id' 		   	: self.pk,
			'user' 	   		: self.user.get_dict(),
			'date' 		   	: self.date
		}


class Lesson_update_detail(models.Model):
	lesson_update_header 	= models.ForeignKey("Lesson_update_header")
	lesson 					= models.TextField(blank=True, null=True)
	to_dos_topic 			= models.ForeignKey("To_dos_topic")


	class Meta:
		app_label = "systech_account"
		db_table  = "lesson_update_detail"


	def get_dict(self):
		return {
			'id' 					: self.pk,
			'lesson_update_header' 	: self.lesson_update_header.get_dict(),
			'lesson' 	   			: self.lesson,
			'to_dos_topic' 			: self.to_dos_topic.get_dict(),
		}