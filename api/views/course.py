from rest_framework.decorators import api_view
from rest_framework.views import APIView
from web_admin.models.course import Course, CourseProgram
from api.serializers.course import CourseSerializer, CourseProgramSerializer
from utils.response_handler import *


class CourseAPIView(APIView):

    @staticmethod
    def save_course_program(course_id, course_programs):

        for course_program in course_programs:

            course_program["course"]  = course_id
            course_program["program"] = course_program["program"].get("uuid")

            serializer = CourseProgramSerializer(data=course_program)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

    def post(self, request):
        try:
            data            = extract_json_data(request)
            company         = get_current_company(request)
            course_programs = data.get("course_programs", None)

            if not course_programs:
                raise_error("No Programs")

            if data.get("uuid", None):
                instance = Course.objects.get(pk=data.get("uuid"))
                serializer = CourseSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer = CourseSerializer(data=data)

            if serializer.is_valid():
                instance = serializer.save()
                self.save_course_program(instance.pk, course_programs)
            else:
                raise_error(serializer.errors)

            return success_response()
        except Exception as e:
            print(e)
            return error_response(str(e))


@api_view(["POST"])
def read_course(request):
    try:
        results = {}
        records = []
        filters = extract_json_data(request)
        company = get_current_company(request)

        if "center_id" in filters:
            q_filters = Q(company=filters["center_id"])
        else:
            q_filters = Q(company=company)

        query_set = Course.objects.filter(q_filters).order_by("-date_created")

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e),show_line=True)


@api_view(["POST"])
def read_course_programs(request):
    try:
        results = {}
        records = []
        filters = extract_json_data(request)
        course_id = filters.get("uuid", None)

        query_set = CourseProgram.objects.filter(course=course_id)

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))