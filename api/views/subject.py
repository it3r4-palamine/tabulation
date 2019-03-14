from rest_framework.decorators import api_view
from rest_framework.views import APIView

from web_admin.models.subject import Subject
from utils import error_messages
from utils.response_handler import *


class SubjectAPIView(APIView):

    def post(self):
        try:
            pass


            return success_response("Success")
        except Exception as e:
            return error_messages(str(e))


@api_view(["POST"])
def read_subjects(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        subjects = Subject.objects.filter(company=company).order_by("-date_created")

        for subject in subjects:
            row = subject.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))
