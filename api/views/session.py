from rest_framework.decorators import api_view
from rest_framework.views import APIView
from web_admin.models.session import *
from api.serializers.session import *


class SessionAPIView(APIView):

    @staticmethod
    def save_session_exercises(session_id, session_exercises):

        for session_exercise in session_exercises:

            uuid = session_exercise.get("uuid", None)

            session_exercise["session"] = session_id
            session_exercise["exercise"] = session_exercise["exercise"].get("id")

            if uuid:
                instance = SessionExercise.objects.get(pk=uuid)
                serializer = SessionExerciseSerializer(data=session_exercise, instance=instance)
            else:
                serializer = SessionExerciseSerializer(data=session_exercise)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

    def post(self, request):
        instance   = None
        is_editing = False
        try:
            data              = extract_json_data(request)
            company           = get_current_company(request)
            session_exercises = data.get("session_exercises", None)

            if not session_exercises:
                raise_error("No Exercises")

            if data.get("uuid", None):
                is_editing  = True
                instance    = Session.objects.get(pk=data.get("uuid"))
                serializer  = SessionSerializer(data=data, instance=instance)
            else:
                data["company"] = company
                serializer = SessionSerializer(data=data)

            if serializer.is_valid():
                instance = serializer.save()
                self.save_session_exercises(instance.pk, session_exercises)

            else:
                raise_error(serializer.errors)

            return success_response()
        except Exception as e:

            if instance and not is_editing:
                instance.delete()

            return error_response(str(e), show_line=True)

    def delete(self, request, uuid):
        instance = Session.objects.get(pk=uuid)
        instance.is_deleted = True
        instance.save()
        SessionExercise.objects.filter(session=uuid).update(is_deleted=True)

        return success_response()


@api_view(["POST"])
def read_student_sessions(request):
    try:
        results = {}
        records = []
        user    = get_current_user(request)

        query_set_enrollment = Session.objects.filter()

        for qs in query_set_enrollment:
            records.append(qs.get_dict())

        # for qse in query_set_enrollment:
        #     query_set_course_programs = CourseProgram.objects.filter(course=qse.course_id)
        #
        #     print(query_set_course_programs.count())
        #
        #     for qs_course_program in query_set_course_programs:
        #         query_set_sessions = ProgramSession.objects.filter(program=qs_course_program.pk)
        #
        #         print(query_set_sessions.count())
        #
        #         for qs_session in query_set_sessions:
        #
        #             session = qs_session.get_dict()
        #             records.append(session)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


@api_view(["POST"])
def read_sessions(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        query_set = Session.objects.filter(company=company,is_deleted=False).order_by("-date_created")

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