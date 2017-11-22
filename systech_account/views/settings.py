from ..forms.assessments import *
from ..forms.multiple_choice import *
from ..models.assessments import *
from ..models.settings import *
from ..forms.settings import *
from ..forms.user_type import *
from ..views.assessments import *
from ..views.common import *


def import_default(request):
	return render(request, 'import/import.html')

def read_module_columns(request, module_type):
	fields = get_fields(request, module_type)

	return success_list(fields,False)

def get_fields(request, module_type):
	t_term = "Transaction Type"
	q_term = "Question"
	terms = get_display_terms(request)
	if terms:
		if terms.transaction_types:
			t_term = terms.transaction_types

		if terms.questions:
			q_term = terms.questions
	fields = {
		"questions" : {
			"question" : {"display" : q_term, "sort" : 2},
			"transaction_type" : {"display" : t_term, "sort" : 3},
			"is_multiple" : {"display" : "Is Multiple Choice", "sort" : 4},
			"code" : {"display" : "Code", "sort" : 1},
			"is_document" : {"display" : "Is Document", "sort" : 5},
			"is_related" : {"display" : "Is Related", "sort" : 6},
			"has_multiple_answer" : {"display" : "Has Multiple Answer", "sort" : 7},
			"is_general" : {"display" : "Is General", "sort" : 8},
			"transaction_types" : {"display" : "General %s"%(t_term), "sort" : 9},
		},
		"choices" : {
			"question" : {"display" : "%s Code"%(q_term), "sort" : 1},
			"value" : {"display" : "Answer", "sort" : 2},
			"is_answer" : {"display" : "Is Answer", "sort" : 3},
			"is_related_required" : {"display" : "Is Related Required", "sort" : 4},
		},
		"effects" : {
			"question" : {"display" : "%s Code"%(q_term), "sort" : 1},
			"value" : {"display" : "Effect", "sort" : 2},
		},
		"findings" : {
			"question" : {"display" : "%s Code"%(q_term), "sort" : 1},
			"value" : {"display" : "Findings", "sort" : 2},
		},
		"recommendations" : {
			"value" : {"display" : "Recommendation", "sort" : 1},
		}
	}
	return fields.get(module_type,{})

def create_dialog(request):
	return render(request, 'import/dialogs/create_dialog.html')

def import_questions(request):
	try:
		data = req_data(request, True)
		data['is_active'] = True

		t_term = "Transaction Type"
		q_term = "Question"
		terms = get_display_terms(request)

		if terms:
			if terms.transaction_types:
				t_term = terms.transaction_types

			if terms.questions:
				q_term = terms.questions

		if 'code' not in data:
			return error("Code is required.")
		else:
			if Assessment_question.objects.filter(code=data['code'],is_active=True).exists():
				return error("Code already exists.")
			else:
				data['code'] = data['code']

		# if 'transaction_type' not in data:
		# 	return error("Transaction Type is required.")
		# else:
		# 	import_transaction_type = clean_string(data['transaction_type'])
		# 	try:
		# 		transaction_type = Transaction_type.objects.get(name__iexact=import_transaction_type,is_active=True)
		# 		data['transaction_type'] = transaction_type.pk
		# 	except Transaction_type.DoesNotExist:
		# 		return error("Transaction Type: "+data['transaction_type'] + " does not exists.")

		if 'question' not in data:
			return error("%s is required."%(q_term))
		else:
			data['value'] = data['question']

		if 'is_multiple' in data:
			is_multiple = clean_string(data['is_multiple'])
			if is_multiple != "Yes" and is_multiple != "No":
				return error("Is Multiple must be 'Yes' or 'No'.")
			if is_multiple == "Yes":
				data['is_multiple'] = True
			else:
				data['is_multiple'] = False
		else:
			return error("Is Multiple must be 'Yes' or 'No'.")

		if 'is_document' in data:
			is_document = clean_string(data['is_document'])
			if is_document != "Yes" and is_document != "No":
				return error("Is Document must be 'Yes' or 'No'.")
			if is_document == "Yes":
				data['is_document'] = True
			else:
				data['is_document'] = False
		else:
			return error("Is Document must be 'Yes' or 'No'.")

		if 'has_multiple_answer' in data:
			has_multiple_answer = clean_string(data['has_multiple_answer'])
			if has_multiple_answer != "Yes" and has_multiple_answer != "No":
				return error("Has Multiple Choice must be 'Yes' or 'No'.")
			if has_multiple_answer == "Yes":
				data['has_multiple_answer'] = True
			else:
				data['has_multiple_answer'] = False
		else:
			return error("Has Multiple Choice must be 'Yes' or 'No'.")

		data['t_types'] = None

		if 'is_general' in data:
			is_general = clean_string(data['is_general'])
			if is_general != "Yes" and is_general != "No":
				return error("Is General must be 'Yes' or 'No'.")
			if is_general == "Yes":
				data['is_general'] = True
				if 'transaction_types' not in data:
					return error("General %s is required."%(t_term))
				else:
					import_transaction_types = clean_string(data['transaction_types'])
					transaction_types = import_transaction_types.split("-")

					transaction_types_id = []
					for transaction_type in transaction_types:
						try:
							data_transaction_type = Transaction_type.objects.get(name__iexact=transaction_type,is_active=True)
							transaction_types_id.append(data_transaction_type.pk)
						except Transaction_type.DoesNotExist:
							return error("%s: "%(t_term)+transaction_type + " does not exists.")

					data['transaction_types'] = list_to_string(transaction_types_id)
					data['t_types'] = transaction_types_id
				data['transaction_type'] = None
			else:
				data['is_general'] = False
				if 'transaction_type' not in data:
					return error("%s is required."%(t_term))
				else:
					import_transaction_type = clean_string(data['transaction_type'])
					try:
						transaction_type = Transaction_type.objects.get(name__iexact=import_transaction_type,is_active=True)
						data['transaction_type'] = transaction_type.pk
					except Transaction_type.DoesNotExist:
						return error("%s: "%(t_term)+data['transaction_type'] + " does not exists.")
				data['transaction_types'] = None

		else:
			# return error("Is General must be 'Yes' or 'No'.")

			if 'transaction_type' not in data:
				return error("%s is required."%(t_term))
			else:
				import_transaction_type = clean_string(data['transaction_type'])
				try:
					transaction_type = Transaction_type.objects.get(name__iexact=import_transaction_type,is_active=True)
					data['transaction_type'] = transaction_type.pk
				except Transaction_type.DoesNotExist:
					return error("%s: "%(t_term)+data['transaction_type'] + " does not exists.")

		if 'is_related' in data:
			is_related_code = clean_string(data['is_related'])
			try:
				assessment_question_code = Assessment_question.objects.get(code=is_related_code,is_active=True)
				data['is_related'] = assessment_question_code.pk
			except Assessment_question.DoesNotExist:
				return error("%s Code: "%(q_term)+is_related_code + " does not exists for Is Related.")

		return_results = create(request,data)
		if return_results != True:
			return error(return_results)

		return success("Successfully Imported.")
	except Exception as e:
		return HttpResponse(e,status=400)

def import_choices(request):
	try:
		data = req_data(request, True)
		data['is_active'] = True
		if 'question' not in data:
			return error("Question Code is required.")
		else:
			try:
				question_code = data['question']
				assessment_question = Assessment_question.objects.get(code=question_code,is_active=True)
				data['question'] = assessment_question.pk
				if 'value' not in data:
					return error("Answer is required.")

				if not assessment_question.is_multiple:
					return error("Question Code: "+ str(question_code) +" is not a multiple choice type.")

				if 'is_answer' in data:
					is_answer = clean_string(data['is_answer'])
					if is_answer != "Yes" and is_answer != "No":
						return error("Is Answer must be 'Yes' or 'No'.")
					if is_answer == "Yes":
						data['is_answer'] = True
					else:
						data['is_answer'] = False
				else:
					return error("Is Answer must be 'Yes' or 'No'.")

				if 'is_related_required' in data:
					is_related_required = clean_string(data['is_related_required'])
					if is_related_required != "Yes" and is_related_required != "No":
						return error("Is Related Required must be 'Yes' or 'No'.")
					if is_related_required == "Yes":
						data['is_related_required'] = True
					else:
						data['is_related_required'] = False
				else:
					return error("Is Related Required must be 'Yes' or 'No'.")

				answer_choice = Choice_form(data)
				if answer_choice.is_valid():
					answer_choice.save()
					choice_data = Choice.objects.filter(question=assessment_question.pk,is_answer=True,is_active=True)
					if len(choice_data) > 1:
						assessment_question.has_multiple_answer = True
						assessment_question.save()

				return success("Successfully Imported.")
			except Assessment_question.DoesNotExist:
				return error("Question doesn't exists.")
	except Exception as e:
		return HttpResponse(e,status=400)

def import_effects(request):
	try:
		data = req_data(request,True)
		data['is_active'] = True
		if 'question' not in data:
			return error("Question Code is required.")
		else:
			try:
				question_code = data['question']
				assessment_question = Assessment_question.objects.get(code=question_code,is_active=True)
				data['question'] = assessment_question.pk

				if 'value' not in data:
					return error("Effect is required.")

				effect_question = Assessment_effect_form(data)
				if effect_question.is_valid():
					effect_question.save()

				return success("Successfully Imported.")
			except Assessment_question.DoesNotExist:
				return error("Question doesn't exists.")
	except Exception as e:
		return HttpResponse(e,status=400)

def import_findings(request):
	try:
		data = req_data(request,True)
		data['is_active'] = True
		if 'question' not in data:
			return error("Question Code is required.")
		else:
			try:
				question_code = data['question']
				assessment_question = Assessment_question.objects.get(code=question_code,is_active=True)
				data['question'] = assessment_question.pk

				if 'value' not in data:
					return error("Findings is required.")

				finding_question = Assessment_finding_form(data)
				if finding_question.is_valid():
					finding_question.save()

				return success("Successfully Imported.")
			except Assessment_question.DoesNotExist:
				return error("Question doesn't exists.")
	except Exception as e:
		return HttpResponse(e,status=400)

def import_recommendations(request):
	try:
		data = req_data(request,True)
		data['is_active'] = True
		if 'value' not in data:
				return error("Recommendation is required.")

		recommendation_question = Assessment_recommendation_form(data)
		if recommendation_question.is_valid():
			recommendation_question.save()

		return success("Successfully Imported.")
	except Exception as e:
		return HttpResponse(e,status=400)

def settings(request):
	return render(request, 'settings/settings.html')

def display_settings(request):
	return render(request, 'settings/display_settings.html')

def display_settings_read(request):
	try:
		data = req_data(request,True)
		records = Display_setting.objects.filter(company=data['company'])

		results = {'data':[]}
		data = []
		for record in records:
			row = record.get_dict()
			data.append(row)

		results['data'] = data

		return success_list(results,False)
	except Exception as e:
		return HttpResponse(e,status=400)

def save_display_terms(request):
	try:
		data = req_data(request,True)
		try:
			instance = Display_setting.objects.get(company=data['company'])
			display_terms = Display_setting_form(data,instance=instance)
		except Display_setting.DoesNotExist:
			display_terms = Display_setting_form(data)

		if display_terms.is_valid():
			display_terms.save()
			return HttpResponse("Successfully saved.",status=200)
		else:
			return HttpResponse(display_terms.errors,status=400)
	except Exception as e:
		return HttpResponse(e,status=400)

def user_types(request):
	return render(request, 'settings/user_types.html')

def read_user_types(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']
		records = User_type.objects.filter(**filters).order_by("id")
		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]
		data = []
		for record in records:
			row = record.get_dict()
			data.append(row)
		results['data'] = data
		return success_list(results,False)
	except Exception as e:
		return HttpResponse(e,status=400)

def user_types_create_dialog(request):
	return render(request, 'settings/dialogs/user_types_create_dialog.html')

def user_types_create(request):
	try: 
		postdata = req_data(request,True)
		try:
			instance = User_type.objects.get(id=postdata.get('id',None))
			user_types = User_type_form(postdata, instance=instance)
		except User_type.DoesNotExist:
			user_types = User_type_form(postdata)

		if user_types.is_valid():
			user_types.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(user_types.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def user_types_delete(request,id=None):
	try:
		try:
			record = User_type.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success()
		except User_type.DoesNotExist:
			raise_error("Recommendation doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)