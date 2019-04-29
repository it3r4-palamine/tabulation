from rest_framework.decorators import api_view
from rest_framework.views import APIView
from api.serializers.exercise import *
from utils.response_handler import *
from web_admin.views.common import generate_pagination


class ExerciseAPIView(APIView):

    def post(self, request):
        try:
            data                = extract_json_data(request)
            exercise            = data.get("exercise", None)
            exercise_questions  = data.get("exercise_questions", None)
            is_assessment_test  = data.get("is_assessment_test", None)
            course              = data.get("course", None)

            if not exercise_questions or len(exercise_questions) == 0:
                raise_error("No Questions")

            if is_assessment_test:
                exercise = dict(
                    transaction_code=data.get("transaction_code"),
                    name=data.get("name"),
                    company=get_current_company(request),
                    is_assessment_test=True,
                    course=course["uuid"]
                )

                if "id" in data:
                    instance = Exercise.objects.get(id=data["id"])
                    serializer = ExerciseSerializer(data=exercise, instance=instance)
                else:
                    serializer = ExerciseSerializer(data=exercise)

                if serializer.is_valid():
                    instance = serializer.save()
                    exercise["id"] = instance.pk
                else:
                    print(serializer.errors)

            for exercise_question in exercise_questions:

                if not exercise_question.get("question"):
                    raise_error("Invalid Question")

                exercise_question["exercise"] = exercise["id"]
                exercise_question["question"] = exercise_question["question"]["uuid"]

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
            return error_response(str(e), show_line=True)

    def delete(self, request, id):
        try:
            print(id)
            query_set = Exercise.objects.get(id=id)
            query_set.delete()
            print(query_set)
            return success_response()
        except Exception as e:
            return error_response(str(e))


@api_view(["POST"])
def read_exercise_questions(request):
    try:
        data    = extract_json_data(request)
        results = {}
        records = []

        query_set = ExerciseQuestion.objects.filter(exercise=data["id"]).order_by()

        for qs in query_set:
            records.append(qs.get_dict())

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


@api_view(["POST"])
def read_exercise(request):
    try:
        results       = {}
        records       = []
        company       = get_current_company(request)
        filters       = extract_json_data(request)
        query_filters = Q(company=company) & Q(is_active=True) & Q(is_deleted=False)
        pagination    = filters.get("pagination")
        limit         = None if pagination else 50
        exercise_type = filters.get("exercise_type")

        if filters.get("search", None):
            search         = filters.get("search")
            query_filters &= Q(name__icontains=search) | Q(transaction_code__icontains=search)

        if exercise_type == "Assessment Test":
            query_filters &= Q(is_assessment_test=True) & Q(is_post_test=False)

        if exercise_type == "Post Test":
            query_filters &= Q(is_post_test=True) & Q(is_assessment_test=False)

        if exercise_type == "Exercise":
            query_filters &= Q(is_post_test=False) & Q(is_assessment_test=False)

        query_set = Exercise.objects.filter(query_filters).order_by("name", "set_no")[:limit]

        for qs in query_set:
            row = qs.get_dict()
            row["question_count"] = qs.get_question_count()
            records.append(row)

        if pagination:
            pagination["limit"] = 30
            pagination["current_page"] = 1
            results.update(generate_pagination(pagination, query_set))
            records = records[results['starting']:results['ending']]

        results["records"] = records

        return success_response(results)
    except Exception as e:
        print(e)
        return error_response(str(e))