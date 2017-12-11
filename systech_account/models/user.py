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
	session_credits  = models.DurationField(blank=True, null=True)
	session_end_date = models.DateTimeField(blank=True, null=True)
	user_intelex_id	 = models.IntegerField(blank=True,null=True)

	USERNAME_FIELD = 'email'

	class Meta:
		app_label = "systech_account"
		db_table  = "User"

	def get_dict(self):
		return {
			"id" : self.pk,
			"fullname" : self.fullname,
		}

	def delete(self):
		self.is_active = False
		self.email += ("__"+str(time.time()))

		self.save()

		return True

class User_type(models.Model):
	name      = models.CharField(max_length=200,blank=True,null=True)
	is_active = models.BooleanField(default=1)
	company   = models.ForeignKey("Company",blank=True,null=True)

	class Meta:
		app_label = "systech_account"
		db_table  = "user_type"

	def get_dict(self):
		return {"id" : self.pk,"name" : self.name,"is_active" : self.is_active}