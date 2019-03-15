from rest_framework.decorators import api_view
from rest_framework.views import APIView

from utils import dict_types
from utils.model_utils import get_next
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


@api_view(["POST"])
def check_reference_no(request):
    try:
        company     = get_current_company(request)
        query_set   = Enrollment.objects.filter(company=company).last()

        if not query_set and query_set.code:
            ref_no = "000000"
        else:
            ref_no = str(query_set.code)

        ref_no = get_next(ref_no)

        return success_response(ref_no)
    except Exception as e:
        return error_response(e, show_line=True)



