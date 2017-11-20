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
from ..models.transaction_types import *
from ..models.assessments import *
from ..models.company import *
from ..views.common import *


def loginpage(request):
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

			if not user.is_admin:
				return error("Invalid account..")

			login(request, user)
			request.session['user_id'] = user.pk

			if user.is_admin: # USER ACCOUNTS
				request.session['admin'] = True

			return success("Logging In...")
		else: return error("Invalid username or password")
	else:
		return redirect("loginpage")

def log_out(request):
	request.session.clear()
	logout(request)
	return redirect("loginpage")