# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# MODELS
from systech_account.models.company import *
from systech_account.models.user import *
from systech_account.models.assessments import *

# OTHERS
from systech_account.views.common import *
import sys, traceback, os


class Get_programs_and_exercises(APIView):
	def post(self, request, *args, **kwargs):
		try:
			# Company renames
			company_rename_list = []
			company_rename_qs = Company_rename.objects.filter(company=request.user.company.pk, is_active=True)

			for company_rename in company_rename_qs:
				company_rename_list.append(company_rename.get_dict())

			# Transaction types
			transaction_type_list = []
			transaction_type_qs = Transaction_type.objects.filter(company=request.user.company.pk, is_active=True)

			for transaction_type in transaction_type_qs:
				transaction_type_list.append(transaction_type.get_dict())

			result = {
				"company_rename_list"	: company_rename_list,
				"transaction_type_list"	: transaction_type_list,
			}

			return Response(result)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print_error(filename, "Get_programs_and_exercises", e, sys.exc_traceback.tb_lineno)
			return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Get_users(APIView):
	def post(self, request, *args, **kwargs):
		try:
			user_list = []
			user_credit_list = []

			user_qs = User.objects.filter(company=request.user.company.pk, is_active=True, user_type__isnull=False).exclude(id=request.user.pk)

			for user in user_qs:
				user_list.append(user.get_dict(True))

				# User credits
				user_credit_qs = User_credit.objects.filter(user=user.pk)
				for _user_credit in user_credit_qs:
					user_credit = _user_credit.get_dict(True)
					user_credit["user"] = user_credit["user"]["id"]
					user_credit_list.append(user_credit)

			result = {
				"user_list"	: user_list,
				"user_credit_list"	: user_credit_list,
			}

			return Response(result)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print_error(filename, "Get_users", e, sys.exc_traceback.tb_lineno)
			return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Get_settings(APIView):
	def post(self, request, *args, **kwargs):
		try:
			recommendation_list = []

			recommendation_qs = Assessment_recommendation.objects.filter(company=request.user.company.pk, is_active=True)

			for recommendation in recommendation_qs:
				recommendation_list.append(recommendation.get_dict())

			result = {
				"recommendation_list" : recommendation_list,
			}

			return Response(result)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print_error(filename, "Get_settings", e, sys.exc_traceback.tb_lineno)
			return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)