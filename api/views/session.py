from rest_framework.decorators import api_view
from rest_framework.views import APIView
from web_admin.models.session import *
from api.serializers.session import *


class SessionAPIView(APIView):

    @staticmethod
    def save_session_exercises(session_id, session_exercises):

        for session_exercise in session_exercises:

            session_exercise["session"] = session_id
            session_exercise["exercise"] = session_exercise["exercise"].get("id")

            serializer = SessionExerciseSerializer(data=session_exercise)

            if serializer.is_valid():
                print("Save")
                serializer.save()
            else:
                print(serializer.errors)

    def post(self, request):
        instance = None
        try:
            data              = extract_json_data(request)
            company           = get_current_company(request)
            session_exercises = data.get("session_exercises", None)

            if not session_exercises:
                raise_error("No Exercises")

            if data.get("uuid", None):
                instance = Session.objects.get(pk=data.get("uuid"))
                serializer = SessionSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer = SessionSerializer(data=data)

            if serializer.is_valid():
                instance = serializer.save()
                self.save_session_exercises(instance.pk, session_exercises)

            else:
                print(serializer.errors)
                raise_error(serializer.errors)

            return success_response()
        except Exception as e:

            if instance:
                instance.delete()

            return error_response(str(e), show_line=True)


@api_view(["POST"])
def read_sessions(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        query_set = Session.objects.filter(company=company).order_by("-date_created")

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


@api_view(["POST"])
def read_session_exercise(request):
    try:
        results    = {}
        records    = []
        filters    = extract_json_data(request)
        session_id = filters.get("uuid", None)

        query_set = SessionExercise.objects.filter(session=session_id).order_by("-date_created")

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))