from django.shortcuts import redirect
from ..views.common import *


class UserMiddleware(object):
	"""Checks if the user is allowed to access the page they are requesting."""

	LOGIN_REDIRECT_URL = ''

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.process_request(request)

	def is_public_page(self, request, first_url):

		public_urls = [
			"logout",
			"admin",
			"select_user",
			"learning_center_signup",
			"sign_in",
		]

		if first_url not in public_urls:
			return self.get_response(request)

	def process_request(self, request):

		# Initialization.
		url = request.path
		urls = url.replace("//", "/").split("/")
		first_url = urls[1]

		if 'HTTP_AUTHORIZATION' in request.META or "api" in first_url:
			return self.get_response(request)

		public_urls = [
			"sign_in",
			"logout",
			"admin",
			"select_user",
			"learning_center_signup",
		]

		student_urls = [
			"student_portal",
		]

		if first_url in public_urls:
			return self.get_response(request)

		if first_url in student_urls and request.user.is_authenticated and request.user.is_student:
			return self.get_response(request)

		if request.user.is_authenticated and request.user.is_student and first_url not in student_urls:
			return redirect("/student_portal/")

		if request.user.is_authenticated and not request.user.is_student and first_url in student_urls:
			return redirect("/")

		not_required_session = [
			"login",
			"logout",
			"signin",
		]

		no_action = [
			"logout",
			"/",
			"",
		]

		if first_url not in not_required_session and not request.user.id:
			if request.method == "GET":
				if first_url not in no_action:
					return redirect("loginpage")

		if first_url in not_required_session and request.user.id:
			if request.method == "GET":
				if first_url not in no_action:
					return redirect("home")

		return self.get_response(request)