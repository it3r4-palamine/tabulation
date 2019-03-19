import re

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

from utils import error_messages
from utils.response_handler import extract_json_data
from ..forms.company import *
from ..forms.user_form import *
from ..models.user import *
from ..views.common import *


def check_if_user_exist(username):
	try:
		return User.objects.get(email=username)
	except User.DoesNotExist:
		raise_error(error_messages.USER_NOT_EXIST)


def authenticate_user(request):
	try:
		data 	 = extract_json_data(request)
		username = data.get("email", None)
		password = data.get("password", None)

		if not username or not password:
			raise_error("Please provide Email and Password")

		if re.match(r"[^@]+@[^@]+\.[^@]+", username):
			user = check_if_user_exist(username)
			username = user.username

		user = authenticate(username=username, password=data['password'])

		if user:
			if not user.is_active:
				return error("Account Inactive. Please activate your account.")

			login(request, user)
			token, created 			   = Token.objects.get_or_create(user=user)
			request.session['token']   = str(token)
			request.session['user_id'] = user.pk
			request.session['company'] = user.company.id if user.company else None

			if user.is_admin:
				request.session['admin'] = True

			if user.is_student:
				return redirect("student_portal")

			return success(request.user.user_type.name)
		else:
			return error("Invalid username or password")

	except Exception as e:
		return error(str(e), show_line=True)


def log_out(request):
	request.session.clear()
	logout(request)
	return redirect("landing_page")


def dashb2oard(request):
	return render(request, "dashboard/dashboard.html")


def dashboard(request):
	return render(request, "dashboard/dashboard.html", { "pagename" : "Student Evaluation"})


def register_company(request):
	company_instance = None
	user_instance    = None
	try:
		data     = extract_json_data(request)
		company  = {}

		if 'name' in data:
			company['name'] = data['name']
		else:
			raise_error(error_messages.LACK_NAME)

		if data['password1'] != data['password2']:
			return error("Password do not match!")

		if Company.objects.filter(name=company["name"]).exists():
			return error("This company name is already taken")

		company_form = CompanyForm(company)

		if company_form.is_valid():
			company_instance = company_form.save()

			data["company"] = company_instance.pk
			data["user_type"]  = 1
			data["is_active"]  = True

			user_form = AdminUserForm(data)

			if user_form.is_valid():
				user_instance = user_form.save()
				login_user(request, user_instance.username, data["password1"])
			else:
				raise_error(user_form.errors)

		else:
			raise_error(company_form.errors)

		return success("Successful")
	except Exception as e:

		if user_instance:
			user_instance.delete()

		if company_instance:
			company_instance.delete()

		return error(e)


def register_student(request):
	user_instance = None
	try:
		data = extract_json_data(request)

		data["username"]  = data["email"].split("@")[0]
		data["is_active"] = True
		data["is_student"] = True
		data["user_type"] = 2
		form = StudentUserForm(data)

		if form.is_valid():
			user_instance = form.save()
			login_user(request, user_instance.username, data["password1"])
		else:
			raise_error(form.errors)

		return success()
	except Exception as e:

		if user_instance:
			user_instance.delete()

		return error(e)


def login_user(request, username, password):
	user = authenticate(username=username, password=password)
	if user:
		login(request, user)
		token, created = Token.objects.get_or_create(user=user)
		request.session['token'] = str(token)
		request.session['user_id'] = user.pk

