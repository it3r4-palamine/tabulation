from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

from ..forms.company import *
from ..forms.user_form import *
from ..forms.user_type import *
from ..models.user import *
from ..views.common import *
from utils.response_handler import extract_json_data

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

			login(request, user)
			token, created = Token.objects.get_or_create(user=user)
			request.session['token']      = str(token)
			request.session['user_id']    = user.pk
			request.session['company_id'] = user.company.id

			# USER ACCOUNTS
			if user.is_admin:
				request.session['admin'] = True

			return success(request.user.user_type.name)
		else:
			return error("Invalid username or password")
	else:
		return redirect("loginpage")

def log_out(request):
	request.session.clear()
	logout(request)
	return redirect("loginpage")

def dashb2oard(request):
	return render(request, "dashboard/dashboard.html")

def dashboard(request):
	return render(request, "dashboard/dashboard.html", {"pagename" : "Student Evaluation"})

def register_company(request):
	company_instance = None
	user_instance    = None
	try:
		data     = extract_json_data(request)
		company  = {}
		print(data)

		if data['password1'] != data['password2']:
			return error("Password do not match!")

		if 'company_name' in data:
			company['name'] = data.get("company_name", None)

		if Company.objects.filter(name=company["name"]).exists():
			return error("This company name is already taken")

		company_form = CompanyForm(company)

		if company_form.is_valid():
			company_instance = company_form.save()

			data["company"] = company_instance.pk
			data["user_type"]  = 1
			data["is_active"]  = True

			user_form = CustomUserCreationForm(data)

			if user_form.is_valid():
				user_instance = user_form.save()
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

			company_form = CompanyForm(company)
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
				password1 = data['password1']
				password2 = data['password2']
				data['company'] = company_data.id
				data['is_admin'] = True
				data['is_active'] = True
				data['email'] = user_email
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


def get_questions_page(request):
	return render(request, "questions/questions.html")

def get_subjects_page(request):
	return render(request, "subjects/subject.html")