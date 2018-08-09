# DJANGO REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# MODELS
from systech_account.models.company import *

# OTHERS
from systech_account.views.common import *
import sys, traceback, os


class Get_programs_and_exercises(APIView):
	def post(self, request, *args, **kwargs):
		try:
			print "Get_programs_and_exercises"
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