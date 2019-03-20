from rest_framework.decorators import api_view
from rest_framework.views import APIView
from web_admin.models.transaction_types import Transaction_type
from api.serializers.exercise import *
from utils.response_handler import *


class ExerciseAPIView(APIView):

    def post(self, request):
        try:
            data                = extract_json_data(request)
            exercise            = data.get("exercise", None)
            exercise_questions  = data.get("exercise_questions", None)

            for exercise_question in exercise_questions:

                exercise_question["exercise"] = exercise["id"]
                exercise_question["question"] = exercise_question["question"]["uuid"]

                print(exercise_question)

                if "uuid" in exercise_question:
                    instance    = ExerciseQuestion.objects.get(pk=exercise_question["uuid"])
                    serializer  = ExerciseQuestionSerializer(data=exercise_question, instance=instance)
                else:
                    serializer  = ExerciseQuestionSerializer(data=exercise_question)

                if serializer.is_valid():
                    serializer.save()
                else:
                    raise_error(serializer.errors)

            return success_response("Success")
        except Exception as e:
            return error_response(e,show_line=True)


@api_view(["POST"])
def read_exercise_questions(request):
    try:
        data    = extract_json_data(request)
        results = {}
        records = []

        query_set = ExerciseQuestion.objects.filter(exercise=data["id"]).order_by()[:100]

        for qs in query_set:
            records.append(qs.get_dict())

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


@api_view(["POST"])
def read_exercise(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        query_set = Transaction_type.objects.filter(company=company,is_active=True).order_by("name", "set_no")[:100]

        for qs in query_set:
            row = qs.get_dict()
            row["question_count"] = qs.get_question_count()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))