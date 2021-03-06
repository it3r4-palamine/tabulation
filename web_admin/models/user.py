# DJANGO
# OTHERS
import time

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# MODELS
from ..models.company import *
from ..models.enrollment import Enrollment


class UserType(models.Model):
	name       = models.CharField(max_length=200, blank=True, null=True)
	is_active  = models.BooleanField(default=1)
	is_default = models.BooleanField(default=0)
	company    = models.ForeignKey("Company", blank=True, null=True, on_delete=models.CASCADE)

	class Meta:
		app_label = "web_admin"
		db_table  = "user_type"

	def get_dict(self):
		return {
			"id" 		 : self.pk,
			"name" 		 : self.name,
			"is_active"  : self.is_active,
			"is_default" : self.is_default
		}


class UserManager(BaseUserManager):

	def create_superuser(self, username, password, email=None):
		if not username:
			raise ValueError('The given email must be set')

		user = self.model(
			username=username,
			password=make_password(password),
			email=email,
		)

		user.is_staff = True
		user.is_admin = True
		user.is_superuser = True
		user.save()
		return user


class User(AbstractBaseUser, PermissionsMixin):

	email            	= models.EmailField(max_length=100, unique=True, null=False, blank=False)
	fullname        	= models.CharField(max_length=100, null=True, blank=True)
	is_admin         	= models.BooleanField(default=False)
	is_staff         	= models.BooleanField(default=False)
	is_active        	= models.BooleanField(default=1)
	user_type        	= models.ForeignKey(UserType, null=True, blank=True, on_delete=models.CASCADE)
	is_edit         	= models.BooleanField(default=False)
	company			 	= models.ForeignKey("Company", blank=True, null=True, on_delete=models.CASCADE)
	is_intelex       	= models.BooleanField(default=False)
	user_intelex_id	 	= models.IntegerField(blank=True,null=True)
	username 		 	= models.CharField(max_length=100, unique=True, null=True, blank=True)
	first_name 		 	= models.CharField(max_length=200, blank=True, null=True)
	last_name 		 	= models.CharField(max_length=200, blank=True, null=True)
	nick_name 		 	= models.CharField(max_length=200, blank=True, null=True)
	address 		 	= models.TextField(blank=True, null=True)
	gender 			 	= models.CharField(max_length=50, blank=True, null=True)
	nationality 	 	= models.CharField(max_length=50, blank=True, null=True)
	date_of_birth 	 	= models.DateField(blank=True, null=True)
	phone_regex 	 	= RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	contact_number 	 	= models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True)
	fathers_name 		= models.CharField(max_length=200, blank=True, null=True)
	mothers_name 		= models.CharField(max_length=200, blank=True, null=True)
	fathers_contact_no 	= models.CharField(max_length=200, blank=True, null=True)
	mothers_contact_no 	= models.CharField(max_length=200, blank=True, null=True)
	guardian_name 		= models.CharField(max_length=200, blank=True, null=True)
	grade_level 		= models.ForeignKey("Gradelevel", blank=True, null=True, on_delete=models.CASCADE)
	school 				= models.ForeignKey("School", blank=True, null=True, on_delete=models.CASCADE)
	description 		= models.TextField(null=True, blank=True)
	rfid				= models.CharField(max_length=20, null=True, blank=True)
	is_student          = models.BooleanField(default=False)
	objects 			= UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		app_label = "web_admin"
		db_table  = "User"

	def get_dict(self, is_local=False, dict_type=DEFAULT):

		instance = {}

		if dict_type == DEFAULT:

			instance = dict()
			instance['id']					= self.pk
			instance['email']				= self.email
			instance['username']			= self.username
			instance['fullname']			= self.fullname
			instance['is_active']			= self.is_active
			instance['is_admin']			= self.is_admin
			instance['password']			= self.password
			instance['is_edit']				= self.is_edit
			instance['first_name']			= self.first_name
			instance['last_name']			= self.last_name
			instance['nick_name']			= self.nick_name
			instance['address']				= self.address
			instance['gender']				= self.gender
			instance['nationality']			= self.nationality
			instance['date_of_birth']		= self.date_of_birth
			instance['contact_number']		= self.contact_number
			instance['fathers_name'] 	  	= self.fathers_name
			instance['mothers_name']		= self.mothers_name
			instance['fathers_contact_no']	= self.fathers_contact_no
			instance['mothers_contact_no']	= self.mothers_contact_no
			instance['grade_level']			= self.grade_level
			instance['school']				= self.school
			instance['description']			= self.description
			instance['rfid']				= self.rfid
			instance['is_intelex']			= self.is_intelex
			instance['user_type']			= self.user_type.get_dict() if self.user_type else None

		if dict_type == UI_SELECT:

			instance = {
				"id" 	    : self.pk,
				"fullname"  : self.fullname,
				"user_type" : self.user_type.get_dict() if self.user_type else None
			}

		if dict_type == DEVICE:

			instance = {
				"id" 			: self.pk,
				"first_name" 	: self.first_name,
				"last_name"  	: self.last_name,
				"fullname"		: self.fullname,
				"rfid"			: self.rfid,
			}

		if is_local:
			instance["username"]  		= self.username
			instance["password"]		= self.password
			instance["user_type"]		= self.user_type.pk if self.user_type else None
			instance["email"]			= self.email
			instance["company"]			= self.company.pk
			instance["is_active"]		= self.is_active
			instance["is_admin"]		= self.is_admin
			instance["is_edit"]			= self.is_edit
			instance["is_intelex"]		= self.is_intelex
			instance["user_intelex_id"] = self.user_intelex_id

		return instance

	def get_full_name(self):
		return self.first_name.join(" ", self.last_name)

	def get_short_name(self):
		return self.username

	def delete(self):
		self.is_active = False
		self.email += ("__"+str(time.time()))
		self.username += ("__"+str(time.time()))

		self.save()

		return True

	def get_active_enrolled_programs(self):
		records = []

		enrollments = Enrollment.objects.filter(user=self.pk,is_active=True,is_deleted=False)

		for enrollment in enrollments:

			if enrollment.get_remaining_credit():
				records.append(enrollment.get_dict(dict_type=DEVICE))

		return records


class UserCredit(models.Model):

	user 			     = models.ForeignKey("User", on_delete=models.CASCADE)
	enrollment_id 	     = models.IntegerField(blank=True, null=True)
	enrollment_code      = models.CharField(max_length=200,blank=True,null=True)
	session_credits      = models.DurationField(blank=True, null=True)
	session_credits_left = models.DurationField(blank=True,null=True)
	session_start_date   = models.DateField(blank=True, null=True)
	session_end_date     = models.DateField(blank=True, null=True)
	program_id	 	     = models.IntegerField(blank=True, null=True)
	program_name	     = models.CharField(max_length=200,blank=True,null=True)

	class Meta:
		app_label = "web_admin"
		db_table  = "user_credits"

	def get_dict(self, is_local=False):

		user_credit = {
			'id' 				   : self.pk,
			'user' 				   : self.user.get_dict(),
			'enrollment_id' 	   : self.enrollment_id,
			'enrollment_code'      : self.enrollment_code,
			'session_credits' 	   : self.session_credits.total_seconds() if self.session_credits else 0,
			'session_credits_left' : self.session_credits_left.total_seconds() if self.session_credits_left else 0,
			'session_start_date'   : self.session_start_date,
			'session_end_date'     : self.session_end_date,
			'program_id' 		   : self.program_id,
			'program_name'		   : self.program_name,
		}

		if is_local:
			user_credit['session_credits'] = self.session_credits
			user_credit['session_credits_left'] = self.session_credits_left

		return user_credit


class UserTimeLog(models.Model):

	user 	 = models.ForeignKey("User", on_delete=models.CASCADE)
	log_type = models.CharField(max_length=20,null=True,blank=True)
	log_time = models.TimeField(blank=True, null=True, default=None)
	log_date = models.DateField(blank=False, null=False, default=timezone.now)
	sync_id  = models.CharField(max_length=50, null=True, blank=True)

	class Meta:
		app_label = "web_admin"
		db_table  = "user_time_logs"


class Lesson_update_header(models.Model):

	user 		 = models.ForeignKey("User", on_delete=models.CASCADE)
	date 		 = models.DateField(blank=True, null=True)
	is_active 	 = models.BooleanField(default=1)

	class Meta:
		app_label = "web_admin"
		db_table  = "lesson_update_header"


	def get_dict(self):
		return {
			'id' 		   	: self.pk,
			'user' 	   		: self.user.get_dict(),
			'date' 		   	: self.date
		}


class Lesson_update_detail(models.Model):
	lesson_update_header 	= models.ForeignKey("Lesson_update_header", on_delete=models.CASCADE)
	lesson 					= models.TextField(blank=True, null=True)
	to_dos_topic 			= models.ForeignKey("To_dos_topic", on_delete=models.CASCADE)


	class Meta:
		app_label = "web_admin"
		db_table  = "lesson_update_detail"


	def get_dict(self):
		return {
			'id' 					: self.pk,
			'lesson_update_header' 	: self.lesson_update_header.get_dict(),
			'lesson' 	   			: self.lesson,
			'to_dos_topic' 			: self.to_dos_topic.get_dict(),
		}