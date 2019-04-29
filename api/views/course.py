from rest_framework.decorators import api_view
from rest_framework.views import APIView

from utils import dict_types
from web_admin.models.course import Course, CourseProgram
from api.serializers.course import CourseSerializer, CourseProgramSerializer
from utils.response_handler import *


class CourseAPIView(APIView):

    def get(self, request, uuid):
        try:
            instance = Course.objects.get(pk=uuid)

            results = instance.get_dict(dict_type=dict_types.COMPLETE)

            return success_response(results)
        except Exception as e:
            return error_response(str(e))

    @staticmethod
    def delete_child(child):
        child.is_deleted = True
        child.save()

    def save_course_program(self, course_id, course_programs):

        for course_program in course_programs:

            if not bool(course_program):
                continue

            uuid                      = course_program.get("uuid", None)
            course_program["course"]  = course_id
            course_program["program"] = course_program["program"].get("uuid")

            if uuid:
                instance = CourseProgram.objects.get(pk=uuid)

                if "is_deleted" in course_program and course_program["is_deleted"]:
                    self.delete_child(instance)
                    continue
                else:
                    serializer = CourseProgramSerializer(data=course_program, instance=instance)
            else:
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
            return error_response(str(e),show_line=True)

    def delete(self, request, uuid):
        instance = Course.objects.get(pk=uuid)
        instance.is_deleted = True
        instance.save()
        CourseProgram.objects.filter(course=uuid).update(is_deleted=True)

        return success_response()


@api_view(["POST"])
def read_course(request):
    try:
        results = {}
        records = []
        filters = extract_json_data(request)
        company = get_current_company(request)
        search  = filters.get("search", None)
        exclude_with_assessment = filters.get("exclude_with_assessment", False)

        if "center_id" in filters:
            q_filters = Q(company=filters["center_id"]) & Q(is_deleted=False)
        else:
            q_filters = Q(company=company) & Q(is_deleted=False)

        if search:
            q_filters &= Q(name__icontains=search) | Q(description__icontains=search)

        query_set = Course.objects.filter(q_filters).order_by("name", "-date_created")

        for qs in query_set:
            row = qs.get_dict()

            if exclude_with_assessment and not row["assessment_test"]:
                continue

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

        query_set = CourseProgram.objects.filter(course=course_id, is_deleted=False)

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))