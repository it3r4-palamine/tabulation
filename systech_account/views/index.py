from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash


from ..forms.transaction_types import *
from ..forms.company import *
from ..forms.user_type import *
from ..models.transaction_types import *
from ..models.assessments import *
from ..models.company import *
from ..forms.user_form import *
from ..models.user import *
from ..views.common import *


def loginpage(request):
	if request.user.id:
		return redirect("home")
	else:
		return render(request, 'login/landing_page.html')

def signin(request):
	if request.user.id:
		return redirect("home")
	else:
		return render(request, 'login/login.html')

def log_in(request):
	if request.method == "POST":
		data = json.loads(request.body.decode("utf-8"))
		user = authenticate(username=data['email'], password=data['password'])

		if user:
			if not user.is_active:
				return error("Account Inactive. Please activate your account.")

			if not user.is_admin or not user.user_type:
				return error("Invalid account..")

			login(request, user)
			request.session['user_id'] = user.pk
			request.session['company_id'] = user.company.id

			if user.is_admin: # USER ACCOUNTS
				request.session['admin'] = True

			return success(request.user.user_type.name)
		else: return error("Invalid username or password")
	else:
		return redirect("loginpage")

def log_out(request):
	request.session.clear()
	logout(request)
	return redirect("loginpage")

def register(request):
	if request.method == "POST":
		data = json.loads(request.body.decode("utf-8"))

		if data['password1'] != data['password2']:
			return error("Password do not match!")
		company = {}
		if 'company_name' in data:
			company['name'] = data['company_name']
			company['is_active'] = True

		if not Company.objects.filter(name=company['name']).exists():
			if User.objects.filter(email=data['email']).exists():
				return error('Email already exists.')

			company_form = Company_form(company)
			if company_form.is_valid():
				company_data = company_form.save()

				user_types = ['Technical','Facilitator','Student']
				user_type_id = None
				for user_type in user_types:
					datus = {}
					datus['name'] = user_type
					datus['is_active'] = True
					datus['is_default'] = True
					datus['company'] = company_data.id
					user_type_form = User_type_form(datus)

					if user_type_form.is_valid():
						user_type_data = user_type_form.save()
						if user_type == 'Technical':
							user_type_id = user_type_data.id

				user_email = data['email']
				user_fullname = data['fullname']
				password1 = data['password1']
				password2 = data['password2']
				data['company'] = company_data.id
				data['is_admin'] = True
				data['is_active'] = True
				data['email'] = user_email
				data['fullname'] = user_fullname
				data['password1'] = password1
				data['password2'] = password2
				data['user_type'] = user_type_id

				user_form = CustomUserCreationForm(data)
				if user_form.is_valid():
					user_data = user_form.save()
				else:
					company_data.delete()
					return error(user_form.errors)
			else:
				return error(company_form.errors)
		else:
			return error("Company already exists.")

		return success("Successfully created!")
	else:
		return redirect("loginpage")
