from rest_framework.decorators import api_view
from rest_framework.views import APIView

from web_admin.models import Enrollment
from utils.response_handler import *


class EnrollmentAPIView(APIView):

    pass


@api_view(["POST"])
def read_enrolled_programs(request):
    try:
        results = {}
        records = []

        enrollments = Enrollment.objects.filter().order_by("-date_created")

        for enrollment in enrollments:
            row = enrollment.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))