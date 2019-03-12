from rest_framework.views import APIView
from web_admin.models import Company
from utils.response_handler import *


class LearningCenterAPI(APIView):

    def get(self, request):
        try:
            results = {}
            records = []

            companies = Company.objects.filter(is_active=True)

            for company in companies:
                records.append(company.get_dict())

            results["records"] = records

            return success_response(results)
        except Exception as e:
            return error_response(e)
