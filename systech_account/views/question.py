from systech_account.models import QuestionType
from utils import error_messages
from utils.response_handler import *
from ..forms.form_question import *
from ..views.common import *


def create(request):
	try:
		data    = extract_json_data(request)
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

		return success("Success")
	except Exception as e:
		return error_http_response(str(e))

def create_choices(pk, choices):

	for choice in choices:
		choice["question"] = pk

		question_choice_form = QuestionChoiceForm(choice)

		if question_choice_form.is_valid():
			record = question_choice_form.save()
		else:
			raise_error("Wrong")


def read_questions(request):
	try:
		results = {}
		records = []

		questions = Question.objects.filter()

		print(len(questions))

		for question in questions:
			row = question.get_dict()
			question_choices = []
			question_choice_records = QuestionChoices.objects.filter(question = question.pk)

			for question_choice in question_choice_records:
				question_choices.append(question_choice.get_dict())

			row["question_choices"] = question_choices

			records.append(row)

		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		return error_http_response(str(e))

def read_question_types(request):
	try:
		results = {}
		records = []

		question_types = QuestionType.objects.filter()

		for question_type in question_types:
			records.append(question_type.get_dict())

		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		return error_http_response(str(e))