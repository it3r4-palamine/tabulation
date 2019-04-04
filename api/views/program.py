from rest_framework.decorators import api_view
from rest_framework.views import APIView
from api.serializers.program import *
from utils.response_handler import *


class ProgramAPIView(APIView):

    @staticmethod
    def delete_child(child):
        child.is_deleted = True
        child.save()

    def save_program_sessions(self, program_id, program_sessions):

        for program_session in program_sessions:

            uuid                       = program_session.get("uuid", None)
            program_session["program"] = program_id
            program_session["session"] = program_session["session"].get("uuid")

            if uuid:
                instance = ProgramSession.objects.get(pk=uuid)

                if "is_deleted" in program_session and program_session["is_deleted"]:
                    self.delete_child(instance)
                    continue
                else:
                    serializer = ProgramSessionSerializer(data=program_session, instance=instance)
            else:
                serializer = ProgramSessionSerializer(data=program_session)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

    def post(self, request):
        instance = None
        try:
            data              = extract_json_data(request)
            company           = get_current_company(request)
            program_sessions  = data.get("program_sessions", None)

            if not program_sessions:
                raise_error("No Sessions")

            if data.get("uuid", None):
                instance = Program.objects.get(pk=data.get("uuid"))
                serializer = ProgramSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer = ProgramSerializer(data=data)

            if serializer.is_valid():
                instance = serializer.save()
                self.save_program_sessions(instance.pk, program_sessions)

            else:
                print(serializer.errors)
                raise_error(serializer.errors)

            return success_response()
        except Exception as e:

            if instance:
                instance.delete()

            return error_response(str(e), show_line=True)


@api_view(["POST"])
def read_programs(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        query_set = Program.objects.filter(company=company,is_deleted=False).order_by("-date_created")

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


# Called in Mobile
@api_view(["POST"])
def read_program_sessions(request):
    try:
        results    = {}
        records    = []
        filters    = extract_json_data(request)
        program_id = filters.get("uuid", None)

        query_set = ProgramSession.objects.filter(program=program_id, is_deleted=False)

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))