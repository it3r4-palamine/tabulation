from rest_framework.decorators import api_view
from rest_framework.views import APIView

from web_admin.views.common import raise_error
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
        record = None
        try:
            data            = extract_json_data(request)
            company         = get_current_company(request)
            choices         = data.get("question_choices", None)
            question_type   = data.get("question_type", None)
            subject         = data.get("subject", None)
            data["company"] = company

            print(data)

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


@api_view(["POST"])
def read_questions(request):
    try:
        results = {}
        records = []
        company = get_current_company(request)

        questions = Question.objects.filter(company=company).order_by("-date_created")

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




