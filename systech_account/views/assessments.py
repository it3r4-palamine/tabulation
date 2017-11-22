from ..forms.assessments import *
from ..models.assessments import *
from ..forms.multiple_choice import *
from ..models.multiple_choice import *
from django.db.models import *
from ..views.common import *


def home(request):
	return render(request, 'assessments/assessment_questions.html')

def create_dialog(request):
	return render(request, 'assessments/dialogs/create_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)

		if 'transaction_type' in data and data['transaction_type']:
			records = Assessment_question.objects.filter(Q(company=data['company'],is_active=True,transaction_type=data['transaction_type']) | Q(company=data['company'],is_active=True,transaction_types__overlap=[data['transaction_type']])).order_by("id")
		else:
			records = Assessment_question.objects.filter(company=data['company'],is_active=True).order_by("id")
		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		datus = []
		for record in records:
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
						t_type = Transaction_type.objects.get(company=data['company'],id=t_types,is_active=True)
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
		return HttpResponse(e, status = 400)

def create(request,results=None):
	try: 
		if results:
			postdata = results
		else:
			postdata = req_data(request,True)
			postdata['value'] = postdata['value']
			# if postdata['is_related']:
			postdata['is_related'] = postdata['is_related']['id'] if 'is_related' in postdata and postdata['is_related'] else None
			transaction_types = postdata.pop('transaction_types',[])

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
		try:
			instance = Assessment_question.objects.get(id=postdata.get('id',None))
			assessment_question = Assessment_question_form(postdata,instance=instance)
		except Assessment_question.DoesNotExist:
			if Assessment_question.objects.filter(company=postdata['company'],code=postdata['code'],is_active=True).exists():
				return error("Code already exists.")
			assessment_question = Assessment_question_form(postdata)
			is_edit = False

		if assessment_question.is_valid():
			assessment_save = assessment_question.save()

			if not is_edit:
				for t_typess in t_types:
					company_assessments = Company_assessment.objects.filter(Q(company=postdata['company'],transaction_type__overlap=[postdata['transaction_type']],is_active=True,is_generated=False) | Q(company=postdata['company'],transaction_type__contains=[t_typess],is_active=True,is_generated=False))
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
						answer_choice = Choice_form(choice,instance=instance_choice)
					except Choice.DoesNotExist:
						answer_choice = Choice_form(choice)

					if answer_choice.is_valid():
						answer_choice.save()

				for effect in effects:
					effect['question'] = assessment_save.pk
					effect['is_active'] = True
					effect['company'] = postdata['company']
					try:
						instance_effect = Assessment_effect.objects.get(id=effect.get('id',None))
						effect_question = Assessment_effect_form(effect,instance=instance_effect)
					except Assessment_effect.DoesNotExist:
						effect_question = Assessment_effect_form(effect)

					if effect_question.is_valid():
						effect_question.save()

				for finding in findings:
					finding['question'] = assessment_save.pk
					finding['is_active'] = True
					finding['company'] = postdata['company']
					try:
						instance_finding = Assessment_finding.objects.get(id=finding.get('id',None))
						finding_question = Assessment_finding_form(finding,instance=instance_finding)
					except Assessment_finding.DoesNotExist:
						finding_question = Assessment_finding_form(finding)

					if finding_question.is_valid():
						finding_question.save()
			if results:
				return True
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(assessment_question.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def delete(request,id = None):
	try:
		try:
			question = Assessment_question.objects.get(pk = id)
			question.is_active = False
			question.save()
			return success()
		except Assessment_question.DoesNotExist:
			raise_error("Record doesn't exist.")
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