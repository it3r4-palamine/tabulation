from rest_framework.decorators import api_view
from rest_framework.views import APIView

from systech_account.views.common import raise_error
from utils import error_messages
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
        try:
            data = extract_json_data(request)
            choices = data.get("question_choices", None)

            if not choices:
                raise_error(error_messages.QUESTION_NO_CHOICES)

            question_form = QuestionSerializer(data=data)

            if question_form.is_valid():
                record = question_form.save()

                if record:
                    self.create_choices(record.pk, choices)
            else:
                raise_error(question_form.errors)

            return success_response("Success")
        except Exception as e:
            print(e)
            return error_response(str(e))

    @staticmethod
    def create_choices(pk, choices):

        for choice in choices:
            choice["question"] = pk

            question_choice_form = QuestionChoiceSerializer(data=choice)

            if question_choice_form.is_valid():
                record = question_choice_form.save()
            else:
                raise_error(question_choice_form.errors)


@api_view(["POST"])
def read_questions(request):
    try:
        results = {}
        records = []

        questions = Question.objects.filter()

        for question in questions:
            row = question.get_dict()
            records.append(row)

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))




