from rest_framework.views import APIView

from systech_account.views.common import raise_error
from utils import error_messages
from utils.response_handler import *


class Question(APIView):

    def post(self, request):
        try:
            data = extract_json_data(request)
            choices = data.get("question_choices", None)

            if not choices:
                raise_error(error_messages.QUESTION_NO_CHOICES)

            question_form = QuestionForm(data)

            if question_form.is_valid():
                record = question_form.save()

                if record:
                    create_choices(record.pk, choices)
            else:
                raise_error(question_form.errors)

        except Exception as e:
            return error_response(e)