from rest_framework.views import APIView
from utils.response_handler import *
from web_admin.models.question import *


class StudentAnswerAPIView(APIView):

    def post(self, request):
        try:
            data = extract_json_data(request)

            print(data)
            query_set = QuestionChoices.objects.filter(pk=data["answer"])

            if query_set:
                if not query_set[0].is_correct:
                    raise_error("Wrong Answer")

            return success_response()
        except Exception as e:
            return error_response(str(e))


