from django.shortcuts import redirect
from ..views.common import *
import json

class User_middleware(object):
	"""Checks if the user is allowed to access the page they are requesting."""

	def process_request(self, request):
		"""The main part of the middleware, called each time a user makes a request."""
		# Initialization.
		url = request.path
		urls = url.replace("//", "/").split("/")
		first_url = urls[1]

		not_required_session = [
			"login",
			"logout",
		]

		modules = [
			"assessments",
			"related_questions",
			"recommendations",
			"company_assessments",
			"transaction_types",
			"company",
			"import",
			"users",
			"settings",
		]

		no_action = [
			"logout",
			"/",
			"",
		]

		if 'HTTP_AUTHORIZATION' in request.META or "api" in first_url:
			return None

		if first_url not in not_required_session and not request.user.id:
			if request.method == "GET":
				if first_url not in no_action:
					return redirect("loginpage")

		if first_url in not_required_session and request.user.id:
			if request.method == "GET":
				if first_url not in no_action:
					return redirect("home")

		# if first_url in modules and request.user.id:
		# 	if "assessments" == first_url:
		# 		if request.user.user_type.name.lower() != 'technical':				
		# 			return redirect("company_assessment_redirect")

		# 	if "related_questions" == first_url:
		# 		if request.user.user_type.name.lower() != 'technical':
		# 			return redirect("company_assessment_redirect")

		# 	if "recommendations" == first_url:
		# 		if request.user.user_type.name.lower() != 'technical':
		# 			return redirect("company_assessment_redirect")

		# 	if "transaction_types" == first_url:
		# 		if request.user.user_type.name.lower() != 'technical':
		# 			return redirect("company_assessment_redirect")

		# 	if "company" == first_url:
		# 		if request.user.user_type.name.lower() != 'technical':
		# 			return redirect("company_assessment_redirect")

		# 	if "import" == first_url:
		# 		if request.user.user_type.name.lower() != 'technical':
		# 			return redirect("company_assessment_redirect")

		# 	if "settings" == first_url:
		# 		if request.user.user_type.name.lower() != 'technical':
		# 			return redirect("company_assessment_redirect")

		return None
