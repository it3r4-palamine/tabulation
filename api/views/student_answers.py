from rest_framework.decorators import api_view
from rest_framework.views import APIView

from api.serializers.student_answer import StudentAnswerSerializer
from utils import response_handler
from utils.response_handler import *
from web_admin.models import StudentAnswer
from web_admin.models.question import *


class StudentAnswerAPIView(APIView):

    def post(self, request):
        answer_ids = []
        try:
            data    = extract_json_data(request)
            user    = get_current_user(request)
            answers = data.get("questions")
            session = data.get("session")
            session_exercise_uuid = data.get("session_exercise")

            if len(answers) == 0:
                raise_error("No Answers received")

            total_correct = 0
            for answer in answers:

                if "answer" not in answer:
                    error_message = dict(title="Invalid submission", message=answer["name"] + " has no answer")
                    raise_error(error_message)

                student_answer = dict(
                    student=user,
                    session=session,
                    session_exercise=session_exercise_uuid,
                    exercise_question=answer["exercise_question"],
                    question=answer["uuid"],
                    answer=answer['answer']
                )

                if QuestionChoices.objects.get(pk=answer["answer"]).is_correct:
                    total_correct += 1

                serializer = StudentAnswerSerializer(data=student_answer)

                if serializer.is_valid():
                    answer_ids.append(serializer.save())
                else:
                    print(serializer.errors)

            result_message = "You scored " + str(total_correct) + "/" + str(len(answers))

            return success_response(result_message)
        except Exception as e:

            if answer_ids:
                for id in answer_ids:
                    id.delete()

            return error_response(response_data=e,show_line=True)


@api_view(["POST"])
def clear_all_answers(request):
    try:
        query_set = StudentAnswer.objects.all().delete()

        return success_response("Succcess")
    except Exception as e:
        return error_response(e)

