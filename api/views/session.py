import math
import random

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from api.serializers.exercise import ExerciseSerializer, ExerciseQuestionSerializer
from utils import dict_types
from web_admin.models import ProgramSession, Enrollment, StudentAnswer, ExerciseQuestion
from web_admin.models.course import CourseProgram
from web_admin.models.session import *
from api.serializers.session import *


class SessionAPIView(APIView):

    @staticmethod
    def delete_child(child):
        child.is_deleted = True
        child.save()

    def save_session_exercises(self, session_id, session_exercises):

        for session_exercise in session_exercises:

            uuid = session_exercise.get("uuid", None)

            session_exercise["session"] = session_id
            session_exercise["exercise"] = session_exercise["exercise"].get("id")

            if uuid:
                instance = SessionExercise.objects.get(pk=uuid)

                if "is_deleted" in session_exercise and session_exercise["is_deleted"]:
                    self.delete_child(instance)

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


# Used in Student Portal
@api_view(["POST"])
def read_student_sessions(request):
    try:
        results = {}
        records = []
        user    = get_current_user(request)

        query_set_enrollments = Enrollment.objects.filter(user=user, is_active=True,is_deleted=False).values("id", "course")

        for enrollment in query_set_enrollments:

            enrollment_id = enrollment.get("id")

            array_program_uuid = CourseProgram.objects.filter(course=enrollment["course"], is_deleted=False).values_list('program', flat=True)
            query_set_sessions = ProgramSession.objects.filter(program__in=array_program_uuid,is_deleted=False)

            for qs in query_set_sessions:
                row = qs.get_dict(dict_type=dict_types.AS_SESSION, enrollment_id=enrollment_id)
                row["enrollment_id"] = enrollment_id
                row["course_id"]     = enrollment["course"]
                records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


# Used in Admin Portal
@api_view(["POST"])
def read_sessions(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        query_set = Session.objects.filter(company=company,is_deleted=False).order_by("name", "-date_created")

        for qs in query_set:
            row = qs.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


# Used in Student Portal
@api_view(["POST"])
def read_session_exercise(request):
    try:
        results       = {}
        records       = []
        filters       = extract_json_data(request)
        session_id    = filters.get("uuid", None)
        enrollment_id = filters.get("enrollment_id", None)
        program_id    = filters.get("program_id", None)

        query_set = SessionExercise.objects.filter(session=session_id, is_deleted=False).order_by("-date_created")

        for qs in query_set:
            row = qs.get_dict()

            if StudentAnswer.objects.filter(enrollment=enrollment_id,
                                            program=program_id,
                                            session_exercise=qs.pk).exists():
                row["has_answered"] = True
                row["score"] = qs.get_exercise_score()

            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


# Used in Student Portal
@api_view(["POST"])
def generate_post_test(request):
    try:
        session             = extract_json_data(request)
        questions           = []
        selected_questions  = []
        query_set_exercises = SessionExercise.objects.filter(session=session["uuid"]).values_list("exercise", flat=True)

        for item in query_set_exercises:
            query_set_record_questions = ExerciseQuestion.objects.filter(exercise=item)
            for qs in query_set_record_questions:
                questions.append(qs.get_dict(dict_type=dict_types.QUESTION_ONLY))

        question_size    = math.ceil(len(questions) / 2)
        random_positions = random.sample(range(len(questions) - 1), question_size)

        for position in random_positions:
            selected_questions.append(questions[position])

        exercise_name = " ".join([session["name"], "Post Test"])
        exercise_code = " ".join([session["name"], "Post Test"])

        exercise = dict(
            name=exercise_name,
            transaction_code=exercise_code,
            company=get_current_company(request),
            is_post_test=True
        )

        serializer = ExerciseSerializer(data=exercise)

        if serializer.is_valid():

            exercise = serializer.save()

            for exercise_question in selected_questions:

                exercise_question["exercise"] = exercise.pk
                exercise_question["question"] = exercise_question["uuid"]

                serializer  = ExerciseQuestionSerializer(data=exercise_question)

                if serializer.is_valid():
                    serializer.save()
                    print("OK sa exercise questions")
                else:
                    print("bad")
                    raise_error(serializer.errors)

            session_exercise = dict(
                session=session["uuid"],
                exercise=exercise.pk
            )

            session_serializer = SessionExerciseSerializer(data=session_exercise)

            if session_serializer.is_valid():
                session_serializer.save()
            else:
                print(session_serializer.errors)

        else:

            if exercise:
                exercise.delete()

            print(serializer.errors)

        return success_response()
    except Exception as e:
        print(e)
        return error_response(str(e))