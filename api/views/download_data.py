# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# MODELS
from web_admin.models.company import *
from web_admin.models.user import *
from web_admin.models.assessments import *
from web_admin.models.company_assessment import *

# OTHERS
from web_admin.views.common import *
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
			transaction_type_qs = Exercise.objects.filter(company=request.user.company.pk, is_active=True)

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
				user_credit_qs = UserCredit.objects.filter(user=user.pk)
				for _user_credit in user_credit_qs:
					user_credit = _user_credit.get_dict(True)
					user_credit["user"] = user_credit["user"]["id"]
					user_credit_list.append(user_credit)

			result = {
				"user_list"			: user_list,
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


class Get_worksheets(APIView):
	def post(self, request, *args, **kwargs):
		try:
			assessment_question_list = []
			assessment_image_list = []
			choice_list = []
			assessment_image_answer_list = []
			multiple_image_answer_list = []
			assessment_effect_list = []
			assessment_finding_list = []

			# Get assessment questions/worksheets
			relateds = ["transaction_type", "parent_question",]
			assessment_question_qs = Assessment_question.objects.filter(company=request.user.company.pk, is_active=True).select_related(*relateds)

			for _assessment_question in assessment_question_qs:
				assessment_question = _assessment_question.get_dict(is_local=True)

				# Get assessment images/worksheet images
				assessment_image_list.extend(assessment_question.pop("images"))

				# Get assessment image answers and multiple image answers
				_assessment_image_answer_list = assessment_question.pop("answers")

				for _assessment_image_answer in _assessment_image_answer_list:
					multiple_image_answer_list.extend(_assessment_image_answer.pop("answer"))

				assessment_image_answer_list.extend(_assessment_image_answer_list)

				# # Get choices
				# choice_qs = Choice.objects.filter(question=assessment_question["id"], is_active=True)

				# for choice in choice_qs:
				# 	choice_list.append(choice.get_dict(True))

				# # Get effects
				# effect_qs = Assessment_effect.objects.filter(question=assessment_question["id"], is_active=True)

				# for effect in effect_qs:
				# 	assessment_effect_list.append(effect.get_dict(True))

				# # Get findings
				# finding_qs = Assessment_finding.objects.filter(question=assessment_question["id"], is_active=True)

				# for finding in finding_qs:
				# 	assessment_finding_list.append(finding.get_dict(True))


				assessment_question_list.append(assessment_question)


			result = {
				"assessment_question_list" 		: assessment_question_list,
				"assessment_image_list" 		: assessment_image_list,
				# "choice_list" 					: choice_list,
				"assessment_image_answer_list" 	: assessment_image_answer_list,
				"multiple_image_answer_list" 	: multiple_image_answer_list,
				# "assessment_effect_list" 		: assessment_effect_list,
				# "assessment_finding_list" 		: assessment_finding_list,
			}

			return Response(result)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print_error(filename, "Get_worksheets", e, sys.exc_traceback.tb_lineno)
			return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Get_sessions(APIView):
	def post(self, request, *args, **kwargs):
		try:
			company_assessment_list = []

			company_assessment_qs = Company_assessment.objects.filter(company=request.user.company.pk, is_active=True, is_synced=False, is_complete=False)

			for company_assessment in company_assessment_qs:
				company_assessment_list.append(company_assessment.get_dict(is_local=True))

			result = {
				"company_assessment_list" : company_assessment_list,
			}

			return Response(result)

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print_error(filename, "Get_sessions", e, sys.exc_traceback.tb_lineno)
			return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)