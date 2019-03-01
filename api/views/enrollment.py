from rest_framework.decorators import api_view
from rest_framework.views import APIView

from utils import dict_types
from web_admin.models import Enrollment
from utils.response_handler import *


class EnrollmentAPIView(APIView):

    pass


@api_view(["POST"])
def read_enrolled_programs(request):
    try:
        results = {}
        records = []

        user = request.user.id

        enrollments = Enrollment.objects.filter(user=user)

        for enrollment in enrollments:
            row = enrollment.get_dict(dict_type=dict_types.DEVICE)
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))