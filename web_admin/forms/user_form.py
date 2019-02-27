from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models.user import *
from ..models.user_logs import *
from django import forms
from django.db.models import Q,F


class CustomUserCreationForm(UserCreationForm):
	"""
	A form that creates a user, with no privileges, from the given email and
	password.
	"""

	def __init__(self, *args, **kargs):
		super(CustomUserCreationForm, self).__init__(*args, **kargs)

	class Meta:
		model  = User
		fields = ("email","fullname", "is_admin","is_active","user_type","is_edit","company","username","first_name","last_name","nick_name","address","gender","nationality","date_of_birth","contact_number","fathers_name","mothers_name","fathers_contact_no","mothers_contact_no","grade_level","school","description")


	def clean(self):
		raw_data = self.cleaned_data
		email = (Q(is_active = True))
		email &= (Q(username=raw_data["username"]) | Q(email = raw_data["email"]))
		instance = User.objects.filter(email)
		if instance.exists():
			instance = instance.first()
			if instance.pk != self.instance.pk and raw_data["email"]:	
				raise ValueError("Email address/Username already in use.")

			if instance.pk != self.instance.pk and raw_data["username"]:
				raise ValueError("Email address/Username already in use.")

		return raw_data


class StudentUserForm(UserCreationForm):
	"""
	A form that creates a user, with no privileges, from the given email and
	password.
	"""

	def __init__(self, *args, **kargs):
		super(StudentUserForm, self).__init__(*args, **kargs)

	class Meta:
		model  = User
		fields = ("email","fullname", "is_admin","is_active","user_type","is_edit","company","is_intelex","user_intelex_id","username","first_name","last_name","nick_name","address","gender","nationality","date_of_birth","contact_number","fathers_name","mothers_name","fathers_contact_no","mothers_contact_no","grade_level","school","description")


	def clean(self):
		raw_data = self.cleaned_data
		email = (Q(is_active = True))
		email &= (Q(username=raw_data["username"]) | Q(email = raw_data["email"]))
		instance = User.objects.filter(email)
		if instance.exists():
			instance = instance.first()
			if instance.pk != self.instance.pk and raw_data["email"]:	
				raise ValueError("Email address/Username already in use.")

			if instance.pk != self.instance.pk and raw_data["username"]:
				raise ValueError("Email address/Username already in use.")

		return raw_data

class CustomUserChangeForm(forms.ModelForm):

	class Meta:
		model  = User
		fields = ("email","fullname", "is_admin","is_active","user_type","is_edit","company","username","first_name","last_name","nick_name","address","gender","nationality","date_of_birth","contact_number","fathers_name","mothers_name","fathers_contact_no","mothers_contact_no","grade_level","school","description","rfid")

	def clean(self):
		raw_data = self.cleaned_data
		# email = (Q(email = raw_data["email"]) & Q(is_active = True))
		email = (Q(is_active = True))
		email &= (Q(username=raw_data["username"]) | Q(email = raw_data["email"]))
		instance = User.objects.filter(email)
		if instance.exists():
			instance = instance.first()
			if instance.pk != self.instance.pk and raw_data["email"]:	
				raise ValueError("Email address/Username already in use.")

			if instance.pk != self.instance.pk and raw_data["username"]:
				raise ValueError("Email address/Username already in use.")

		return raw_data

class SetPasswordForm(forms.ModelForm):
	"""
	A form that lets a user change set their password without entering the old
	password
	"""
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model  = User
		fields = ('email', 'fullname', 'is_active')


	def clean_new_password2(self):
		raw_data = self.cleaned_data
		password1 = raw_data.get('password1')
		password2 = raw_data.get('password2')
		if password1 and password2:
			if password1 != password2:
				raise ValueError("Password didn't match.")
			   
		return password2

class User_credit_form(forms.ModelForm):
	class Meta:
		model  = User_credit
		fields = ('user','enrollment_id','enrollment_code','session_credits','session_end_date','program_id','program_name','session_start_date')

class UserLogForm(forms.ModelForm):

	class Meta:
		model = UserLogs
		fields = ('user','device')