from rest_framework.decorators import api_view
from rest_framework.views import APIView
from web_admin.models import Course
from api.serializers.course import CourseSerializer
from utils.response_handler import *


class CourseAPIView(APIView):

    def post(self, request):
        try:
            data = extract_json_data(request)
            company = get_current_company(request)

            if data.get("uuid", None):
                instance = Course.objects.get(pk=data.get("uuid"))
                serializer = CourseSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer = CourseSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

            return success_response()
        except Exception as e:
            return error_response(e)


@api_view(["POST"])
def read_course(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        subjects = Course.objects.filter(company=company).order_by("-date_created")

        for subject in subjects:
            row = subject.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))