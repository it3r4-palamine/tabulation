import uuid

from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from root import settings
from web_admin.models import ExerciseQuestion, StudentAnswer
from web_admin.views.common import raise_error, generate_pagination
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


# Used in Admin Page for loading questions
@api_view(["POST"])
def read_questions(request):
    try:
        results    = {}
        records    = []
        filters    = extract_json_data(request)
        company    = get_current_company(request)
        pagination = filters.get("pagination")
        search     = filters.get("search", None)
        limit      = None if pagination else 50
        q_filters  = Q(company=company) & Q(is_deleted=False)

        if search:
            q_filters &= Q(name__icontains=search) | Q(description__icontains=search)

        query_set = Question.objects.filter(q_filters).order_by("-date_created")[:limit]

        for qs in query_set:
            question_choices = []
            question_choices_record = QuestionChoices.objects.filter(question=qs.uuid)

            for question_choice in question_choices_record:
                question_choices.append(question_choice.get_dict())

            row = qs.get_dict()
            row["question_choices"] = question_choices
            records.append(row)

        if pagination:
            pagination["limit"] = 30
            pagination["current_page"] = 1
            results.update(generate_pagination(pagination, query_set))
            records = records[results['starting']:results['ending']]

        results["records"] = records

        return success_response(results)
    except Exception as e:
        return error_response(str(e))


@api_view(["POST"])
def write_question_image(request):
    try:
        data = request.POST
        files = request.FILES
        uploaded_file = files["inventory_image"]
        inventory_id = data["uuid"]

        # Get File Name
        filename = uploaded_file.name

        # Extract File Extension
        ext = filename.split('.')[-1]

        # Generate UUID for Filename
        file_uuid = uuid.uuid4()
        filename = "%s.%s" % (file_uuid, ext)
        record = Question.objects.get(uuid=inventory_id)

        if record.default_image and str(record.default_image) != "/media/default_inventory.jpg":
            file_path = settings.BASE_DIR + str(record.default_image)

            if os.path.isfile(file_path):
                os.remove(file_path)

        fs = FileSystemStorage()
        filename = fs.save(filename, uploaded_file)
        uploaded_file_url = fs.url(filename)

        record.default_image = uploaded_file_url
        record.save()

        return success_response("Image Uploaded")
    except Exception as e:
        return error_http_response(str(e), show_line=True)


# Used in Questionnaire Module
# Student Portal, used to retrieve questions when selecting a exercises
@api_view(["POST"])
def read_exercise_questions(request):
    try:
        data      = extract_json_data(request)
        records   = []
        results   = {}
        query_set = []

        # Prepare Required Parameters for reading question and answers
        session_uuid          = data.get("session", None)
        session_exercise_uuid = data.get("session_exercise", None)
        exercise_uuid         = data.get("exercise", None)
        enrollment_id         = data.get("enrollment_id", None)
        program_id            = data.get("program_id", None)

        # For Assessment Test
        is_assessment_test    = data.get("is_assessment_test", False)

        if not is_assessment_test and (not session_uuid or not session_exercise_uuid or not exercise_uuid):
            raise_error("Something went wrong")
        elif is_assessment_test:
            query_set = ExerciseQuestion.objects.filter(exercise=exercise_uuid,is_deleted=False)
        else:
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




