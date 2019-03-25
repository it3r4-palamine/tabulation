from rest_framework.views import APIView
from utils.response_handler import *


class StudentAnswerAPIView(APIView):

    def post(self, request):
        try:
            data = extract_json_data(request)

            print(data)

            return success_response()
        except Exception as e:
            return error_response(str(e))


