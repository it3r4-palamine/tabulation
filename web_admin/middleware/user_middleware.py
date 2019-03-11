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
		"""The main part of the middleware, called each time a user makes a request."""
		# Initialization.
		url = request.path
		urls = url.replace("//", "/").split("/")
		first_url = urls[0]

		try:
			second_url = urls[1]
		except IndexError:
			second_url = None

		if 'HTTP_AUTHORIZATION' in request.META or "api" in first_url:
			return self.get_response(request)

		public_urls = [
			"sign_in",
			"logout",
			"admin",
			"select_user",
			"learning_center_signup",
		]

		print(first_url)

		if first_url in public_urls:
			return self.get_response(request)

		# self.is_public_page(request, first_url)

		if first_url == "student_portal" and second_url == "login" and request.user.is_authenticated():
			return redirect("/student_portal/dashboard/")

		if first_url == "student_portal" and request.user.is_authenticated():
			return self.get_response(request)

		if first_url == "student_portal" and second_url == "login":
			return self.get_response(request)

		if first_url == "student_portal" and second_url == "login_employee":
			return self.get_response(request)

		if first_url == "student_portal" and not request.user.is_authenticated():
			return redirect("/student_portal/login/")

		if first_url == "student_portal" and second_url == "login":
			return self.get_response(request)

		if first_url == "student_portal":
			return self.get_response(request)

		# if not request.user.is_anonymous() and request.user.is_authenticated() and request.user.is_student and not first_url == "student_portal":
		# 	return redirect("/student_portal/")

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

	def redirect_to(self, page, error_message=None, actually_redirect=True):
		"""Redirects the user to another page.

        Keyword arguments:
        page -- the page to redirect the user to.
        error_message -- the error message to print to the terminal (default: None)
        actually_redirect -- used for testing. If False, the error message is printed but no actual redirection is done. (default: True)
        """
		if error_message:
			print("AUTHENTICATION ERROR: " + error_message)

		if actually_redirect:
			return redirect(page, permanent=True)
		else:
			return None
