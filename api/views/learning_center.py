from rest_framework.views import APIView
from web_admin.models import Company
from utils.response_handler import *


class LearningCenterAPI(APIView):

    def get(self, request, center_id = None):
        try:
            results = {}
            records = []

            if center_id:
                company = Company.objects.get(id=center_id,is_active=True).get_dict()
                results["record"] = company
            else:
                companies = Company.objects.filter(is_active=True)

                for company in companies:
                    records.append(company.get_dict())

                results["records"] = records

            return success_response(results)
        except Exception as e:
            return error_response(e)
