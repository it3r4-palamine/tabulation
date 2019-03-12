from ..forms.assessments import *
from ..forms.multiple_choice import *
from ..models.assessments import *
from ..models.settings import *
from ..forms.settings import *
from ..forms.company import *
from ..forms.user_type import *
from ..forms.transaction_types import *
from ..views.assessments import *
from ..views.common import *
from ..views.sentence_matching import *
from utils.view_utils import *

import sys, traceback, os

def import_default(request):
	if request.user.user_type.name.lower() != "technical":
		return redirect("company_assessment_redirect")
	else:
		return render(request, 'import/import.html')

def read_module_columns(request, module_type):
	fields = get_fields(request, module_type)

	return success_list(fields,False)

def get_fields(request, module_type):
	t_term = "Transaction Type"
	q_term = "Question"
	p_term = "Company"
	terms = get_display_terms(request)
	if terms:
		if terms.transaction_types:
			t_term = terms.transaction_types

		if terms.questions:
			q_term = terms.questions

		if terms.company_rename:
			p_term = terms.company_rename
	fields = {
		"questions" : {
			"code" : {"display" : "Code", "sort" : 1},
			"question" : {"display" : q_term, "sort" : 2},
			"transaction_type" : {"display" : t_term, "sort" : 3},
			"set_no" : {"display" : t_term + " Set No.", "sort" : 4},
			"is_multiple" : {"display" : "Is Multiple Choice", "sort" : 5},
			"answer_type" : {"display" : "Answer Type", "sort" : 6},
			"is_document" : {"display" : "Is Document", "sort" : 7},
			"parent_question" : {"display" : "Is Follow up", "sort" : 8},
			"has_multiple_answer" : {"display" : "Has Multiple Answer", "sort" : 9},
			"is_general" : {"display" : "Is General", "sort" : 10},
			"transaction_types" : {"display" : "General %s"%(t_term), "sort" : 11},
			"has_follow_up" : {"display" : "Has Follow up", "sort" : 12},
		},
		"choices" : {
			"question" : {"display" : "%s Code"%(q_term), "sort" : 1},
			"value" : {"display" : "Answer", "sort" : 2},
			"is_answer" : {"display" : "Is Answer", "sort" : 3},
			"follow_up_required" : {"display" : "Is Follow up Required", "sort" : 4},
			"required_document_image" : {"display" : "Required Document Image", "sort" : 5},
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
		},
		"transaction_types" : {
			"name" : {"display" : "Name", "sort" : 1},
			"transaction_code" : {"display" : "Code", "sort" : 2},
			"set_no" : {"display" : "Set No.", "sort" : 3},
			"program_assigned" : {"display" : p_term, "sort" : 4},
		}
	}
	return fields.get(module_type,{})

def create_dialog(request):
	return render(request, 'import/dialogs/create_dialog.html')

def upload_dialog(request):
	return render(request, 'import/dialogs/upload_dialog.html')

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

		if data['is_multiple'] == False:
			if 'answer_type' in data:
				answer_type = clean_string(data['answer_type'])
				if answer_type != "Text" and answer_type != "Number":
					return error("Answer Type must be 'Text' or 'Number'.")
				
				data['answer_type'] = answer_type
			else:
				return error("Answer Type must be 'Text' or 'Number'.")

		if 'has_follow_up' in data:
			has_follow_up = clean_string(data['has_follow_up'])
			if has_follow_up != "Yes" and has_follow_up != "No":
				return error("Has Follow up must be 'Yes' or 'No'.")
			if has_follow_up == "Yes":
				data['has_follow_up'] = True
			else:
				data['has_follow_up'] = False
		else:
			return error("Has Follow up must be 'Yes' or 'No'.")

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
							data_transaction_type = Transaction_type.objects.get(name__iexact=transaction_type,is_active=True,set_no=data['set_no'])
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
						transaction_type = Transaction_type.objects.get(name__iexact=import_transaction_type,is_active=True,set_no=data['set_no'])
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
					transaction_type = Transaction_type.objects.get(name__iexact=import_transaction_type,is_active=True,set_no=data['set_no'])
					data['transaction_type'] = transaction_type.pk
				except Transaction_type.DoesNotExist:
					return error("%s: "%(t_term)+data['transaction_type'] + " does not exists.")

		if 'parent_question' in data:
			is_related_code = clean_string(data['parent_question'])
			try:
				assessment_question_code = Assessment_question.objects.get(code=is_related_code,is_active=True)
				data['parent_question'] = assessment_question_code.pk
			except Assessment_question.DoesNotExist:
				return error("%s Code: "%(q_term)+is_related_code + " does not exists for Is Follow up.")

		return_results = create(request,data)
		if return_results != True:
			return error(return_results)

		return success("Successfully Imported.")
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		linenum = sys.exc_traceback.tb_lineno,
		print(filename)
		print(linenum)
		print(e)
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
				else:
					result = sentence_matching(data.get('value',None),"Choice",assessment_question.pk)
					if result:
						return error("Answer already exists: '" + result + "'")

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

				if 'follow_up_required' in data:
					follow_up_required = clean_string(data['follow_up_required'])
					if follow_up_required != "Yes" and follow_up_required != "No":
						return error("Is Follow up Required must be 'Yes' or 'No'.")
					if follow_up_required == "Yes":
						data['follow_up_required'] = True
					else:
						data['follow_up_required'] = False
				else:
					return error("Is Follow up Required must be 'Yes' or 'No'.")

				if 'required_document_image' in data:
					required_document_image = clean_string(data['required_document_image'])
					if required_document_image != "Yes" and required_document_image != "No":
						return error("Required Document Image must be 'Yes' or 'No'.")
					if required_document_image == "Yes":
						data['required_document_image'] = True
					else:
						data['required_document_image'] = False
				else:
					return error("Required Document Image must be 'Yes' or 'No'.")

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
				else:
					result = sentence_matching(data.get('value',None),"Assessment_effect",assessment_question.pk)
					if result:
						return error("Effect already exists: '" + result + "'")

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
				else:
					result = sentence_matching(data.get('value',None),"Assessment_finding",assessment_question.pk)
					if result:
						return error("Findings already exists: '" + result + "'")

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
		else:
			result = sentence_matching(data.get('value',None),"Assessment_recommendation",None)
			if result:
				return error("Recommendation already exists: '" + result + "'")

		recommendation_question = Assessment_recommendation_form(data)
		if recommendation_question.is_valid():
			recommendation_question.save()

		return success("Successfully Imported.")
	except Exception as e:
		return HttpResponse(e,status=400)

def import_transaction_types(request):
	try:
		data = req_data(request,True)
		data['is_active'] = True

		if 'name' not in data:
			return error("Name is requried.")

		if 'transaction_code' not in data:
			return error("Code is required.")

		if 'set_no' not in data:
			return error("Set No. is required.")

		check_transaction_type = Transaction_type.objects.filter(company=data['company'],transaction_code__iexact=data['transaction_code'],name__iexact=data['name'],is_active=True,set_no=data['set_no']).first()
		if check_transaction_type:
			return error(data['name'] + " already exists.")

		transaction_code_form = Transaction_type_form(data)

		if transaction_code_form.is_valid():
			transaction_type_save = transaction_code_form.save()

			if 'program_assigned' in data:
				import_programs = clean_string(data['program_assigned'])
				programs = import_programs.split(",")

				for program in programs:
					try:
						has_program = Company_rename.objects.get(company=data['company'],name__iexact=str(program),is_active=True)

						t_type = has_program.transaction_type
						t_type.append(transaction_type_save.pk)

						t_types 					= {}
						t_types['program_id'] 		= has_program.program_id
						t_types['is_active'] 		= has_program.is_active
						t_types['is_intelex'] 		= has_program.is_intelex
						t_types['company'] 			= data['company']
						t_types['name'] 			= has_program.name
						t_types['transaction_type'] = list_to_string(t_type)

						company_rename_form = Company_rename_form(t_types,instance=has_program)

						if company_rename_form.is_valid():
							company_rename_form.save()

					except Company_rename.DoesNotExist:
						raise_error(program + " does not exists.")
		return success("Successfully Imported.")
	except Exception as e:
		return HttpResponse(e,status=400)

def settings(request):
	if request.user.user_type.name.lower() != "technical":
		return redirect("company_assessment_redirect")
	else:
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
			row['user_type'] = request.user.user_type.name
			row['user_type_id'] = request.user.id
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
		
		filters 			 = {}
		filters['is_active'] = True
		filters['company']   = data['company']
		
		records = UserType.objects.filter(**filters).order_by("id")
		
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
			instance = UserType.objects.get(id=postdata.get('id', None))
			user_types = User_type_form(postdata, instance=instance)
		except UserType.DoesNotExist:
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
			record = UserType.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success("Successfully deleted.")
		except UserType.DoesNotExist:
			raise_error("User doesn't exists.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def to_dos(request):
	return render(request, 'settings/to_dos.html')

def read_to_dos(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)

		filters 		 	 = {}
		filters['is_active'] = True
		filters['company']	 = data['company']

		records = To_dos_topic.objects.filter(**filters).order_by("id")

		results = {'data': []}
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

def to_dos_create_dialog(request):
	return render(request, 'settings/dialogs/to_dos_create_dialog.html')

def to_dos_create(request):
	try:
		postdata = req_data(request,True)
		try:
			instance = To_dos_topic.objects.get(id=postdata.get('id',None))
			to_dos = To_dos_topic_form(postdata, instance=instance)
		except To_dos_topic.DoesNotExist:
			to_dos = To_dos_topic_form(postdata)

		if to_dos.is_valid():
			to_dos.save()
			return HttpResponse("Successfully saved.",status=200)
		else:
			return HttpResponse(to_dos.errors,status=400)
	except Exception as e:
		return HttpResponse(e,status=400)

def to_dos_delete(request,id=None):
	try:
		try:
			record 			 = To_dos_topic.objects.get(pk=id)
			record.is_active = False
			record.save()
			return success("Successfully deleted.")
		except To_dos_topic.DoesNotExist:
			raise_error("Topic doesn't exists.")
	except Exception as e:
		return HttpResponse(e,status=400)

def math_symbols(request):
	return render(request, 'settings/math_symbols.html')

def math_symbols_create_dialog(request):
	return render(request, 'settings/dialogs/math_symbols_create_dialog.html')

def math_symbols_create(request):
	try: 
		postdata = req_data(request,True)
		try:
			instance = Math_symbol.objects.get(id=postdata.get('id',None))
			math_symbols = Math_symbol_form(postdata, instance=instance)
		except Math_symbol.DoesNotExist:
			math_symbols = Math_symbol_form(postdata)

		if math_symbols.is_valid():
			math_symbols.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(math_symbols.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def read_math_symbols(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']
		records = Math_symbol.objects.filter(**filters).order_by("id")
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

def math_symbols_delete(request,id=None):
	try:
		try:
			record = Math_symbol.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success("Successfully deleted.")
		except Math_symbol.DoesNotExist:
			raise_error("Symbol doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def schools(request):
	return render(request, 'settings/schools.html')

def schools_create_dialog(request):
	return render(request, 'settings/dialogs/schools_create_dialog.html')

def read_schools(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']
		records = School.objects.filter(**filters).order_by("id")
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

def schools_delete(request,id=None):
	try:
		try:
			record = School.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success("Successfully deleted.")
		except School.DoesNotExist:
			raise_error("Symbol doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def schools_create(request):
	try: 
		postdata = req_data(request,True)
		try:
			instance = School.objects.get(id=postdata.get('id',None))
			schools = School_form(postdata, instance=instance)
		except School.DoesNotExist:
			schools = School_form(postdata)

		if schools.is_valid():
			schools.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(schools.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def grade_levels(request):
	return render(request, 'settings/grade_levels.html')

def grade_levels_create_dialog(request):
	return render(request, 'settings/dialogs/grade_levels_create_dialog.html')

def read_grade_levels(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']
		records = GradeLevel.objects.filter(**filters).order_by("id")
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

def grade_levels_delete(request,id=None):
	try:
		try:
			record = GradeLevel.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success("Successfully deleted.")
		except GradeLevel.DoesNotExist:
			raise_error("Symbol doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def grade_levels_create(request):
	try: 
		postdata = req_data(request,True)
		try:
			instance = GradeLevel.objects.get(id=postdata.get('id',None))
			schools = Grade_level_form(postdata, instance=instance)
		except GradeLevel.DoesNotExist:
			schools = Grade_level_form(postdata)

		if schools.is_valid():
			schools.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(schools.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def trainer_notes(request):
	return render(request, 'settings/trainer_notes.html')

def trainer_notes_create_dialog(request):
	return render(request, 'settings/dialogs/trainer_notes_create_dialog.html')

def read_trainer_notes(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		filters = {}
		filters['is_active'] = True
		records = TrainerNote.objects.filter(**filters).order_by("id")
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

def trainer_notes_create(request):
	try:
		postdata = req_data(request,True)
		record_id = postdata.get("id", None)

		if record_id:
			instance = TrainerNote.objects.get(id=record_id)
			form = TrainerNoteForm(postdata,instance=instance)
		else:
			form = TrainerNoteForm(postdata)

		if form.is_valid():
			form.save()
		else:
			raise_error(form.errors)

		return success("Success")
	except Exception as e:
		return HttpResponse(str(e), status = 400)





