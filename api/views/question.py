from rest_framework.decorators import api_view
from rest_framework.views import APIView

from web_admin.models import ExerciseQuestion, StudentAnswer
from web_admin.views.common import raise_error
from utils import error_messages, dict_types, response_handler
from utils.response_handler import *
from api.serializers.question import *


class QuestionAPIView(APIView):

    def get(self, request, uuid):
        try:
            question_choices        = []
            question                = Question.objects.get(pk=uuid)
            question_choices_record = QuestionChoices.objects.filter(question=uuid)

            for question_choice in question_choices_record:
                question_choices.append(question_choice.get_dict())

            results = question.get_dict()
            results["question_choices"] = question_choices

            return success_response(results)
        except Question.DoesNotExist:
            return error_response(error_messages.RECORD_DOES_NOT_EXIST)

    def post(self, request):
        record = None
        try:
            data            = extract_json_data(request)
            company         = get_current_company(request)
            choices         = data.get("question_choices", None)
            question_type   = data.get("question_type", None)
            subject         = data.get("subject", None)
            data["company"] = company

            if question_type:
                data["question_type"] = question_type.get("uuid")

            if subject:
                data["subject"] = subject.get("uuid")

            if not choices:
                raise_error(error_messages.QUESTION_NO_CHOICES)

            # Update
            if data.get("uuid", None):
                instance = Question.objects.get(pk=data.get("uuid"))
                serializer = QuestionSerializer(data=data, instance=instance)
            else:
                serializer = QuestionSerializer(data=data)

            if serializer.is_valid():
                record = serializer.save()

                if record:
                    self.create_choices(record.pk, choices)
            else:
                raise_error(serializer.errors)

            return success_response("Success")
        except Exception as e:

            if record:
                record.delete()

            return error_response(str(e))

    @staticmethod
    def create_choices(pk, choices):

        for choice in choices:
            choice["question"] = pk

            if choice.get("uuid", None):
                instance   = QuestionChoices.objects.get(pk=choice.get("uuid"))
                serializer = QuestionChoiceSerializer(data=choice, instance=instance)
            else:
                serializer = QuestionChoiceSerializer(data=choice)

            if serializer.is_valid():
                serializer.save()
            else:
                raise_error(serializer.errors)

    def delete(self, request, uuid):

        if ExerciseQuestion.objects.filter(question=uuid).exists():
            return error_response("This question has been assigned to an exercise, You can't delete this question. You need to remove it before deleting this")

        instance = Question.objects.get(pk=uuid)
        instance.is_deleted = True
        instance.save()
        QuestionChoices.objects.filter(question=uuid).update(is_deleted=True)

        return success_response(response_data=response_handler.DELETE_SUCCESS)


@api_view(["POST"])
def read_questions(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        questions = Question.objects.filter(company=company, is_deleted=False).order_by("-date_created")

        for question in questions:
            question_choices = []
            question_choices_record = QuestionChoices.objects.filter(question=question.uuid)

            for question_choice in question_choices_record:
                question_choices.append(question_choice.get_dict())

            row = question.get_dict()
            row["question_choices"] = question_choices
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


# Used in Questionnaire Module
# Student Portal, used to retrieve questions when selecting a exercises
@api_view(["POST"])
def read_exercise_questions(request):
    try:
        data = extract_json_data(request)
        records = []
        results = {}

        # Prepare Required Parameters for reading question and answers
        session_uuid          = data.get("session", None)
        session_exercise_uuid = data.get("session_exercise", None)
        exercise_uuid         = data.get("exercise", None)
        enrollment_id         = data.get("enrollment_id", None)
        program_id            = data.get("program_id", None)

        if not session_uuid or not session_exercise_uuid or not exercise_uuid:
            raise_error("Something went wrong")

        query_set = ExerciseQuestion.objects.filter(exercise=exercise_uuid,is_deleted=False)

        for qs in query_set:
            row = qs.get_dict(dict_type=dict_types.QUESTION_ONLY)

            try:
                query_set = StudentAnswer.objects.get(enrollment=enrollment_id,
                                                      program_id=program_id,
                                                      session=session_uuid,
                                                      session_exercise=session_exercise_uuid,
                                                      exercise_question=qs.pk,
                                                      question=qs.question.pk)

                row = qs.get_dict(dict_type=dict_types.QUESTION_W_ANSWER)
                row["answer"] = query_set.answer.pk
                row["answered_correct"] = query_set.answer.is_correct

            except StudentAnswer.DoesNotExist:
                pass

            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))




