from ..forms.assessments import *
from ..models.assessments import *
from ..forms.multiple_choice import *
from ..models.multiple_choice import *
from django.db.models import *
from ..views.common import *
from ..views.sentence_matching import *


def home(request):
	if request.user.user_type.name.lower() != "technical":
		return redirect("company_assessment_redirect")
	else:
		return render(request, 'assessments/assessment_questions.html')

def create_dialog(request):
	return render(request, 'assessments/dialogs/create_dialog.html')

def upload_dialog(request):
	return render(request, 'assessments/dialogs/upload_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		pagination = None

		code = data.pop("code","")

		filters = (Q(company=data['company'],is_active=True))

		if 'pagination' in data:
			pagination = data.pop("pagination",None)

		if 'transaction_type' in data and data['transaction_type']:
			if isinstance(data['transaction_type'],list):
				filters &= (Q(is_active=True,transaction_type__in=data['transaction_type']) | Q(is_active=True,transaction_types__overlap=data['transaction_type']))
			else:	
				filters &= (Q(is_active=True,transaction_type=data['transaction_type']) | Q(is_active=True,transaction_types__overlap=[data['transaction_type']]))
			# records = Assessment_question.objects.filter(Q(is_active=True,transaction_type=data['transaction_type']) | Q(is_active=True,transaction_types__overlap=[data['transaction_type']])).order_by("id")
		
		if code:
			filters &= (Q(code__icontains=code) | Q(value__icontains=code) | Q(transaction_type__name__icontains=code))

		sort_by = generate_sorting(data.pop("sort",None))
		questionsIds = []
		if 'type' in data:
			related_questions = Related_question.objects.filter(is_active=True)
			for related_question in related_questions:
				for ids in related_question.related_questions:
					questionsIds.append(ids)

			records = Assessment_question.objects.filter(filters).exclude(id__in=questionsIds).order_by(*sort_by)
		else:
			records = Assessment_question.objects.filter(filters).order_by(*sort_by)

		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		datus = []
		for record in records:
			if 'all' in data:
				row = record.get_dict()
			else:
				general_transaction_types = []
				row = record.get_dict()
				choices = Choice.objects.filter(company=data['company'],question=record.pk,is_active=True)
				answers = []
				for choice in choices:
					answer_choice = choice.get_dict()
					answers.append(answer_choice)

				effects = Assessment_effect.objects.filter(company=data['company'],question=record.pk,is_active=True)
				possible_effect = []
				for effect in effects:
					effect_question = effect.get_dict()
					possible_effect.append(effect_question)

				findings = Assessment_finding.objects.filter(company=data['company'],question=record.pk,is_active=True)
				possible_finding = []
				for finding in findings:
					finding_question = finding.get_dict()
					possible_finding.append(finding_question)
				if record.transaction_types:
					for t_types in record.transaction_types:
						try:
							t_type = str2model("Transaction_type").objects.get(company=data['company'],id=t_types,is_active=True)
						except Transaction_type.DoesNotExist:
							continue
						transaction_type_dict = {'id':t_type.pk,'name':t_type.name,'is_active':t_type.is_active}
						general_transaction_types.append(transaction_type_dict)

				row['transaction_types'] = general_transaction_types
				row['choices'] = answers
				row['effects'] = possible_effect
				row['findings'] = possible_finding

			datus.append(row)

		results['data'] = datus
		return success_list(results,False)
	except Exception as e:
		cprint(e)
		return HttpResponse(e, status = 400)

def generate_code(request):
	try:
		data = req_data(request,True)
		new_code = True
		if data['is_general']:
			filters = {'is_general' : True}
			transaction_code = "GENE"
		else:
			# filters = {'is_general' : False,"transaction_type__id" : data['transaction_type']['id'],"transaction_type__transaction_code" : data['transaction_type']['transaction_code']}
			filters = {'is_general' : False,"transaction_type__transaction_code" : data['transaction_type']['transaction_code']}
			try:
				transaction_code = str2model("Transaction_type").objects.get(exercise_id=data['transaction_type']['exercise_id'],set_no=data['transaction_type']['set_no'],is_active=True,company=data['company'],transaction_code=data['transaction_type']['transaction_code']).transaction_code
			except Exception as e:
				return error("No code.")

			if 'id' in data:
				instance = Assessment_question.objects.get(id=data['id'])
				transaction_type_id = instance.transaction_type.pk
				
				if data['transaction_type']['id'] != transaction_type_id:
					questionUsed = Assessment_answer.objects.filter(question=instance.id,company_assessment__is_active=True,transaction_type=transaction_type_id).first()
					if questionUsed:
						return error("Question is currently in use.")
				
				if data['transaction_type']['id'] == transaction_type_id:
					last_code = instance.code
					new_code = False

		questions = Assessment_question.objects.filter(**filters).last()

		if new_code:
			if not questions:
				last_code = transaction_code + "000001"
			else:
				# if len(questions.code) != 10:
				# 	cprint("QQQQ")
				# 	last_code = transaction_code + "000001"
				# else:
				code = questions.code
				last_code = code[-1:]
				if last_code.isdigit():
					last_code = str(int(last_code) + 1)
					if len(last_code) == 1:
						last_code = code[:-1] + last_code
					else:
						last_code = code[:-2] + last_code
				else:
					last_code += " - 1"
			
		return success(last_code)

	except Exception as e:
		raise e

def create(request,results=None):
	try: 
		if results:
			postdata = results
		else:
			postdata = req_data(request,True)
			postdata['value'] = postdata['value']
			# if postdata['parent_question']:
			postdata['parent_question'] = postdata['parent_question']['id'] if 'parent_question' in postdata and postdata['parent_question'] else None
			transaction_types = postdata.pop('transaction_types',[])
			old_is_related = postdata.pop('old_is_related',None)

			terms = get_display_terms(request)
			term = "transaction types"
			if terms:
				if terms.transaction_types:
					term = terms.transaction_types

			if 'is_general' in postdata:
				if postdata['is_general'] == True:
					if not transaction_types:
						return error("Please select %s."%(term))
				else:
					if 'transaction_type' not in postdata:
						return error("Please select %s."%(term))
			else:
				if 'transaction_type' not in postdata:
					return error("Please select %s."%(term))

			# else:
			# 	data['code'] = data['code']

			general_transaction_types = []
			t_type = []
			if transaction_types:
				postdata['transaction_type'] = None
			else:
				postdata['transaction_type'] = postdata['transaction_type']['id']
				t_type.append(postdata['transaction_type'])
				# general_transaction_types.append(postdata['transaction_type'])
			for transaction_type in transaction_types:
				general_transaction_types.append(transaction_type['id'])
				t_type.append(transaction_type['id'])

			postdata['t_types'] = t_type
			postdata['transaction_types'] = list_to_string(general_transaction_types)
			postdata['company'] = postdata['company']
		choices = postdata.pop("choices",None)
		effects = postdata.pop("effects",None)
		findings = postdata.pop("findings",None)
		t_types = postdata.pop("t_types",None)
		is_edit = True

		if postdata['is_multiple']:
			postdata['answer_type'] = None

		try:
			instance = Assessment_question.objects.get(id=postdata.get('id',None))
			assessment_question = Assessment_question_form(postdata,instance=instance)
		except Assessment_question.DoesNotExist:
			create_filters = {
				'company' : postdata['company'],
				'code' : postdata['code'],
				'is_active' : True
			}
			if not postdata['is_general']:
				create_filters['transaction_type'] = postdata['transaction_type']
			if Assessment_question.objects.filter(**create_filters).exists():
				return error("Code already exists.")
			assessment_question = Assessment_question_form(postdata)
			is_edit = False

		if assessment_question.is_valid():
			assessment_save = assessment_question.save()

			if is_edit:
				if assessment_save.parent_question:
					condition = old_is_related and assessment_save.parent_question.id != old_is_related
				else:
					condition = old_is_related
				
				if condition:
					is_related_assessment = Assessment_question.objects.filter(parent_question=old_is_related)
					if len(is_related_assessment) < 1:
						old_is_related_assessment = Assessment_question.objects.filter(id=old_is_related).update(has_follow_up=False)

				Assessment_question.objects.filter(id=postdata.get('parent_question',None)).update(has_follow_up=True)

			if not is_edit and t_types:
				for t_typess in t_types:
					company_assessments = str2model("Company_assessment").objects.filter(Q(company=postdata['company'],transaction_type__overlap=[postdata['transaction_type']],is_active=True,is_generated=False) | Q(company=postdata['company'],transaction_type__contains=[t_typess],is_active=True,is_generated=False))
					for assessments in company_assessments:
						no_answer = Decimal(0)
						for company_assessments_ttypes in assessments.transaction_type:
							questions = Assessment_question.objects.filter(Q(company=postdata['company'],transaction_types__contains=[t_typess],is_active=True) | Q(company=postdata['company'],transaction_type=t_typess,is_active=True))
						for question in questions:
							try:
								answers = Assessment_answer.objects.get(company=postdata['company'],transaction_type=t_typess,company_assessment=assessments.pk,question=question.pk)
								continue
							except Assessment_answer.DoesNotExist:
								no_answer += 1
						if not assessments.is_generated and no_answer > 0:
							assessments.is_complete = False
							assessments.save()
			
			if not results:
				for choice in choices:
					choice['question'] = assessment_save.pk
					choice['is_active'] = True
					choice['company'] = postdata['company']
					try:
						instance_choice = Choice.objects.get(id=choice.get('id',None))
						result = sentence_matching(choice.get('value',None),"Choice",assessment_save.pk,instance_choice.pk)
						answer_choice = Choice_form(choice,instance=instance_choice)
					except Choice.DoesNotExist:
						result = sentence_matching(choice.get('value',None),"Choice",assessment_save.pk)
						
						answer_choice = Choice_form(choice)

					if result:
						return error("Answer already exists: '" + result + "'")

					if answer_choice.is_valid():
						answer_choice.save()

				for effect in effects:
					effect['question'] = assessment_save.pk
					effect['is_active'] = True
					effect['company'] = postdata['company']
					try:
						instance_effect = Assessment_effect.objects.get(id=effect.get('id',None))
						result = sentence_matching(effect.get('value',None),"Assessment_effect",assessment_save.pk,instance_effect.pk)
						effect_question = Assessment_effect_form(effect,instance=instance_effect)
					except Assessment_effect.DoesNotExist:
						result = sentence_matching(effect.get('value',None),"Assessment_effect",assessment_save.pk)

						effect_question = Assessment_effect_form(effect)

					if result:
						return error("Effect already exists: '" + result + "'")

					if effect_question.is_valid():
						effect_question.save()

				for finding in findings:
					finding['question'] = assessment_save.pk
					finding['is_active'] = True
					finding['company'] = postdata['company']
					try:
						instance_finding = Assessment_finding.objects.get(id=finding.get('id',None))
						result = sentence_matching(finding.get('value',None),"Assessment_finding",assessment_save.pk,instance_finding.pk)
						finding_question = Assessment_finding_form(finding,instance=instance_finding)
					except Assessment_finding.DoesNotExist:
						result = sentence_matching(finding.get('value',None),"Assessment_finding",assessment_save.pk)
						
						finding_question = Assessment_finding_form(finding)
					
					if result:
						return error("Findings already exists: '" + result + "'")

					if finding_question.is_valid():
						finding_question.save()
			if results:
				return True
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(assessment_question.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def upload(request):
	if request.method == "POST":
		try:
			data = request.POST
			files = request.FILES
			images = files.getlist("images")
			# if len(files) == 0:
			# 	raise_error("Kindly select a file first.")

			
			company = get_current_company(request)
			datus = {}
			old_is_related = data.pop('old_is_related',None)
			datus['uploaded_question'] = True
			datus['is_document'] = data['is_document']
			datus['code'] = data['code']
			datus['company'] = company
			datus['is_active'] = True
			datus['transaction_type'] = data['transaction_type']

			effects = data.pop("effects",None)
			findings = data.getlist("findings")
			data.pop("images",None)
			# data.pop("findings",None)
			answers = data.pop("answers",None)

			timer = data['timer'] if 'timer' in data else None
			datus['timer'] = timer

			# data["code"] = "6666666366"
			# datus["code"] = data["code"]

			try:
				instance = Assessment_question.objects.get(id=data.get('id',None))
				assessment_question = Assessment_question_form(datus,instance=instance)
			except Assessment_question.DoesNotExist:
				create_filters = {
					'company' : company,
					'code' : data['code'],
					'is_active' : True
				}
				if Assessment_question.objects.filter(**create_filters).exists():
					return error("Code already exists.")
				assessment_question = Assessment_question_form(datus)

			if assessment_question.is_valid():
				assessment_save = assessment_question.save()
				for image in images:
					image_F = {}
					image_F["image"] = image
					image_F["filename"] = image
					image_F["filelocation"] = image

					image_Q = {}
					image_Q['question'] = assessment_save.pk
					image_Q['is_active'] = True
					image_Q['company'] = company
					image_Q['image'] = image

					image_question = Assessment_image_form(image_Q, image_F)

					if image_question.is_valid():
						image_question.save()
			# saveData(request, data, assessment_save.pk)
			return success(assessment_save.pk)
		except Exception as e:
			return error(e)
	else: return error('method error')

def multiple_upload(request):
	if request.method == "POST":
		try:
			data = request.POST
			files = request.FILES
			images = files.getlist("images")
			company = get_current_company(request)

			data.pop("images",None)
			datus = {}
			datus['is_active'] = True

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
				# if Assessment_question.objects.filter(code=data['code'],is_active=True).exists():
				# 	return error("Code already exists.")
				# else:
				datus['code'] = data['code']

			# datus['is_document'] = data['is_document']
			datus['company'] = company
			datus['uploaded_question'] = True
			datus['transaction_type'] = data['transaction_type']
			try:
				instance = Assessment_question.objects.get(code=data['code'],transaction_type=data['transaction_type'],is_active=True)
				assessment_question = Assessment_question_form(datus,instance=instance)
			except Assessment_question.DoesNotExist:
				assessment_question = Assessment_question_form(datus)

			if assessment_question.is_valid():
				assessment_save = assessment_question.save()
				for image in images:
					image_F = {}
					image_F["image"] = image
					image_F["filename"] = image
					image_F["filelocation"] = image

					image_Q = {
						'question' : assessment_save.pk,
						'is_active' : True,
						'company' : company,
						'image' : image
					}

					image_question = Assessment_image_form(image_Q, image_F)
					if image_question.is_valid():
						image_question.save()
						return success(assessment_save.pk)
					else: raise_error(json.dumps(image_question.errors))
			else: raise_error(json.dumps(assessment_question.errors))
		except Exception as e:
			return error(e)
	else: return error("method error")


def saveData(request):
	try:
		postdatus = req_data(request,True)
		postdata = postdatus['datus']
		company = get_current_company(request)
		q_id = postdatus['id']
		answers = postdata.pop("answers",None)
		effects = postdata.pop("effects",None)
		findings = postdata.pop("findings",None)

		for effect in effects:
			effect['question'] = q_id
			effect['is_active'] = True
			effect['company'] = company
			try:
				instance_effect = Assessment_effect.objects.get(id=effect.get('id',None))
				result = sentence_matching(effect.get('value',None),"Assessment_effect",q_id,instance_effect.pk)
				effect_question = Assessment_effect_form(effect,instance=instance_effect)
			except Assessment_effect.DoesNotExist:
				result = sentence_matching(effect.get('value',None),"Assessment_effect",q_id)

				effect_question = Assessment_effect_form(effect)

			if result:
				return error("Effect already exists: '" + result + "'")

			if effect_question.is_valid():
				effect_question.save()

		for finding in findings:
			finding['question'] = q_id
			finding['is_active'] = True
			finding['company'] = company
			try:
				instance_finding = Assessment_finding.objects.get(id=finding.get('id',None))
				result = sentence_matching(finding.get('value',None),"Assessment_finding",q_id,instance_finding.pk)
				finding_question = Assessment_finding_form(finding,instance=instance_finding)
			except Assessment_finding.DoesNotExist:
				result = sentence_matching(finding.get('value',None),"Assessment_finding",q_id)
				
				finding_question = Assessment_finding_form(finding)
			
			if result:
				return error("Findings already exists: '" + result + "'")

			if finding_question.is_valid():
				finding_question.save()

		for answer in answers:
			answer['question'] = q_id
			answer['is_active'] = True
			answer['company'] = company

			multiple_answers = answer.pop("answer",[])
			try:
				instance_answer = Assessment_image_answer.objects.get(id=answer.get('id',None))
				answer_question = Assessment_image_answer_form(answer,instance=instance_answer)
			except Assessment_image_answer.DoesNotExist:
				answer_question = Assessment_image_answer_form(answer)

			if answer_question.is_valid():
				answer_pk = answer_question.save()

				for multiple_answer in multiple_answers:
					multiple_answer['image_answer'] = answer_pk.pk

					try:
						instance_multiple_answer = Multiple_image_answer.objects.get(id=multiple_answer.get('id',None))
						multiple_answer_question = Multiple_image_answer_form(multiple_answer,instance=instance_multiple_answer)
					except Multiple_image_answer.DoesNotExist:
						multiple_answer['is_active'] = True
						multiple_answer_question = Multiple_image_answer_form(multiple_answer)

					if multiple_answer_question.is_valid():
						multiple_answer_question.save()
					else:
						raise_error(json.dumps(multiple_answer_question.errors))


		return HttpResponse("Successfully saved.", status = 200)
	except Exception as err:
		return HttpResponse(err, status = 400)

def multiple_upload_answer_keys(request):
	try:
		postdatus = req_data(request,True)
		postdata = postdatus['datus']
		company = get_current_company(request)
		q_id = postdatus['id']
		answer_keys = postdata

		for answer_key in answer_keys:
			answer_key['question'] = q_id
			answer_key['is_active'] = True
			answer_key['company'] = company

			multiple_answers = answer_key.pop("answer",[])

			answer_key_form = Assessment_image_answer_form(answer_key)
			if answer_key_form.is_valid():
				answer_pk = answer_key_form.save()

				for multiple_answer in multiple_answers:
					multiple_answer['image_answer'] = answer_pk.pk
					multiple_answer['is_active'] = True

					multiple_answer_question = Multiple_image_answer_form(multiple_answer)

					if multiple_answer_question.is_valid():
						multiple_answer_question.save()
					else:
						raise_error(json.dumps(multiple_answer_question.errors))

		return success()
	except Exception as err:
		return HttpResponse(err,status=400)

def delete(request,id = None):
	try:
		try:
			question = Assessment_question.objects.get(pk = id)
			question.is_active = False

			questionUsed = Assessment_answer.objects.filter(question=id,company_assessment__is_active=True).first()
			if questionUsed:
				raise_error("Question is currently in use.")
			else:
				question.save()

			return success("Successfully deleted.")
		except Assessment_question.DoesNotExist:
			raise_error("Question doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def delete_choice(request,id = None):
	try:
		try:
			choice = Choice.objects.get(pk = id)
			choice.is_active = False
			choice.save()
			return success("Successfully deleted.")
		except Choice.DoesNotExist:
			raise_error("Choice doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def delete_effect(request,id = None):
	try:
		try:
			effect = Assessment_effect.objects.get(pk = id)
			effect.is_active = False
			effect.save()
			return success("Successfully deleted.")
		except Assessment_effect.DoesNotExist:
			raise_error("Effect doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def delete_finding(request,id = None):
	try:
		try:
			finding = Assessment_finding.objects.get(pk = id)
			finding.is_active = False
			finding.save()
			return success("Successfully deleted.")
		except Assessment_finding.DoesNotExist:
			raise_error("Finding doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def delete_image(request,id = None):
	try:
		try:
			image = Assessment_image.objects.get(pk = id)
			image.is_active = False
			image.save()
			return success("Successfully deleted.")
		except Assessment_image.DoesNotExist:
			raise_error("Image doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def delete_answer(request,id = None):
	try:
		try:
			answer = Assessment_image_answer.objects.get(pk = id)
			answer.is_active = False
			answer.save()
			return success("Successfully deleted.")
		except Assessment_image_answer.DoesNotExist:
			raise_error("Answer doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def delete_multiple_answer(request,id = None):
	try:
		try:
			answer = Multiple_image_answer.objects.get(pk = id)
			answer.is_active = False
			answer.save()
			return success("Successfully deleted.")
		except Multiple_image_answer.DoesNotExist:
			raise_error("Answer doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def related_questions(request):
	if request.user.user_type.name.lower() != "technical":
		return redirect("company_assessment_redirect")
	else:
		return render(request, 'assessments/related_questions.html')

def read_related_questions(request):
	try:
		data = req_data(request,True)
		pagination = None

		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']

		if 'pagination' in data:
			pagination = data.pop("pagination",None)

		records = Related_question.objects.filter(**filters).order_by('id')
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

def related_questions_create_dialog(request):
	return render(request, 'assessments/dialogs/related_questions_create_dialog.html')

def related_questions_create(request):
	try:
		data = req_data(request,True)
		related_questions = data.pop('related_questions',[])

		related_questionsArr = []
		for related_question in related_questions:
			related_questionsArr.append(related_question['id'])

		data['related_questions'] = list_to_string(related_questionsArr)

		try:
			instance = Related_question.objects.get(id=data.get('id',None))
			related_questions_form = Related_question_form(data,instance=instance)
		except Related_question.DoesNotExist:
			related_questions_form = Related_question_form(data)

		if related_questions_form.is_valid():
			related_questions_form.save()

			questionsIds = []
			related_questions = Related_question.objects.filter(is_active=True)
			for related_question in related_questions:
				for ids in related_question.related_questions:
					questionsIds.append(ids)

			questions = Assessment_question.objects.filter(is_active=True)
			for question in questions:
				if question.pk in questionsIds:
					question.has_related = True
				else:
					question.has_related = False
				question.save()
			return HttpResponse("Successfully saved.",status=200)
		else:
			return HttpResponse(related_questions_form.errors,status=400)
	except Exception as e:
		return HttpResponse(e,status=400)

def delete_related_questions(request,id = None):
	try:
		try:
			related_question = Related_question.objects.get(pk = id)
			related_question.is_active = False
			related_question.save()
			return success("Successfully deleted.")
		except Related_question.DoesNotExist:
			raise_error("Related question doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)