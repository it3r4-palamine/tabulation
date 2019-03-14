from rest_framework.decorators import api_view
from rest_framework.views import APIView

from api.serializers.subject import SubjectSerializer
from api.serializers.program import ProgramSerializer
from web_admin.models.subject import Subject
from web_admin.models.program import Program
from utils.response_handler import *


class ProgramAPIView(APIView):

    def post(self, request):
        try:
            data    = extract_json_data(request)
            company = get_current_company(request)

            if data.get("uuid", None):
                instance = Program.objects.get(pk=data.get("uuid"))
                serializer = SubjectSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer = ProgramSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

            return success_response()
        except Exception as e:
            return error_response(e)


class SubjectAPIView(APIView):

    def post(self, request):
        try:
            data    = extract_json_data(request)
            company = get_current_company(request)

            if data.get("uuid", None):
                instance = Subject.objects.get(pk=data.get("uuid"))
                serializer = SubjectSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer      = SubjectSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

            return success_response("Success")
        except Exception as e:
            return error_response(str(e))


@api_view(["POST"])
def read_programs(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        query_set = Program.objects.filter(company=company).order_by()

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


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
