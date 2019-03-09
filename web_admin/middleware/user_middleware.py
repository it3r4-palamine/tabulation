from django.shortcuts import redirect
from ..views.common import *


class UserMiddleware(object):
	"""Checks if the user is allowed to access the page they are requesting."""

	def process_request(self, request):
		"""The main part of the middleware, called each time a user makes a request."""
		# Initialization.
		url = request.path
		urls = url.replace("//", "/").split("/")
		first_url = urls[1]

		try:
			second_url = urls[2]
		except IndexError:
			second_url = None

		if 'HTTP_AUTHORIZATION' in request.META or "api" in first_url:
			return None

		if first_url == "logout":
			return None

		if first_url == "admin":
			return None

		if first_url == "learning_center_signup":
			return None

		if first_url == "student_portal" and second_url == "login" and request.user.is_authenticated():
			return redirect("/student_portal/dashboard/")

		if first_url == "student_portal" and request.user.is_authenticated():
			return None

		if first_url == "student_portal" and second_url == "login":
			return None

		if first_url == "student_portal" and second_url == "login_employee":
			return None

		if first_url == "student_portal" and not request.user.is_authenticated():
			return redirect("/student_portal/login/")

		if first_url == "student_portal" and second_url == "login":
			return None

		if first_url == "student_portal":
			return None

		if not request.user.is_anonymous() and request.user.is_authenticated() and request.user.is_student and not first_url == "student_portal":
			return redirect("/student_portal/")

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

		return None
