from rest_framework.decorators import api_view
from rest_framework.views import APIView

from api.serializers.enrollment import EnrollmentSerializer
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
            row = enrollment.get_dict(dict_type=dict_types.STUDENT)
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


@api_view(["POST"])
def enroll_course(request):
    try:
        data        = extract_json_data(request)
        user        = get_current_user(request)
        course_id   = data.get("uuid", None)
        company     = data.get("company", None)

        enrollment = dict(
            user=user,
            course=course_id,
            company=company)

        serializer = EnrollmentSerializer(data=enrollment)

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return success_response()
    except Exception as e:
        print(e)
        return error_response(str(e), show_line=True)


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



