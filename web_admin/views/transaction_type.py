from django.shortcuts import redirect

from ..forms.exercise import *
from ..models.assessments import *
from ..models.company import *
from ..views.common import *
import sys, os
import requests
import time

def transaction_type(request):
	if request.user.user_type.name.lower() != "technical":
		return redirect("company_assessment_redirect")
	else:
		return render(request, 'transaction_type/transaction_type.html')

def create_dialog(request):
	return render(request, 'transaction_type/dialogs/create_dialog.html')

def read(request):
	try:
		data 				 = req_data(request,True)
		filters 			 = Q(is_active=True) & Q(company=data['company'])
		name_search 	   	 = data.pop("name","")
		has_company 	   	 = data.get("company_rename",None)
		bypass_code_exists 	 = data.get("bypass_code_exists",False)
		with_questions		 = data.get("with_questions",False)
		c_term 			   	 = "Company"
		terms 				 = get_display_terms(request)

		if terms:
			if terms.company_rename:
				c_term = terms.company_rename
		if has_company:
			try:
				company 		  = Company_rename.objects.get(id=has_company)

				if with_questions:
					t_types_ids = []
					t_types = Exercise.objects.filter(id__in=company.transaction_type)
					for t_type in t_types:
						check_question = Assessment_question.objects.filter(is_active=True,company=data['company'],transaction_type=t_type.id)
						if len(check_question) > 0:
							t_types_ids.append(t_type.id)

					filters &= Q(id__in=t_types_ids)
				else:
					filters &= Q(id__in=company.transaction_type)

			except Company_rename.DoesNotExist:
				raise_error("%s doesn't exist."%(c_term))

		has_ids = data.get('ids',None)
		if has_ids:
			filters &= Q(id__in=has_ids)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)

		if name_search:
			filters &= Q(name__icontains=name_search) | Q(transaction_code__icontains=name_search)

		sort_by = generate_sorting(data.pop("sort",None))

		if 'program_id' in data:
			records = Exercise.objects.filter(filters).exclude(id__in=data['program_id']).order_by(*sort_by)
		else:
			records = Exercise.objects.filter(filters).order_by(*sort_by)

		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]

		data = []
		for record in records:
			row = record.get_dict()
			if not bypass_code_exists:
				row['code_exist'] = False
				if row['transaction_code']:
					questions = Assessment_question.objects.filter(code__startswith=row['transaction_code'])
					if questions:
						row['code_exist'] = True
			
			data.append(row)

		results['data'] = data
		return success_list(results,False)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		return HttpResponse(e, status = 400)

def create(request):
	try: 
		postdata = req_data(request,True)
		try:
			instance = Exercise.objects.get(company=postdata['company'], id=postdata.get('id', None), is_active=True)
			try:
				check_transaction_type = Exercise.objects.filter(company=postdata['company'], transaction_code__iexact=postdata['transaction_code'], name__iexact=postdata['name'], is_active=True, set_no=postdata['set_no']).first()
				if check_transaction_type:
					if check_transaction_type.pk != postdata['id']: 
						return error(check_transaction_type.name + " already exists.")

				transaction_type = ExerciseForm(postdata, instance=instance)
			except Exercise.DoesNotExist:
				transaction_type = ExerciseForm(postdata, instance=instance)
		except Exercise.DoesNotExist:
			try:
				check_transaction_type = Exercise.objects.get(company=postdata['company'], transaction_code__iexact=postdata['transaction_code'], name__iexact=postdata['name'], is_active=True, set_no=postdata['set_no'])
				return error(check_transaction_type.name + " already exists.")
			except Exercise.DoesNotExist:
				transaction_type = ExerciseForm(postdata)

		if(transaction_type.is_valid()):
			transaction_type.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(transaction_type.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def delete(request,id = None):
	try:
		data = req_data(request,True)
		t_term = "Transaction Type"
		terms = get_display_terms(request)
		if terms:
			if terms.transaction_types:
				t_term = terms.transaction_types
		use_in_questions = Assessment_question.objects.filter(company=data['company'],transaction_type=id,is_active=True).first()
		# use_in_companies = Company.objects.filter(transaction_type__contains=[id],is_active=True)
		if use_in_questions:
			raise_error("This %s is currently in use."%(t_term))
		try:
			record = Exercise.objects.get(pk = id)
			record.is_active = False
			record.transaction_code = str(record.transaction_code) + str(time.mktime(time.gmtime()))
			record.save()
			return success("Successfully deleted.")
		except Exercise.DoesNotExist:
			raise_error("%s doesn't exist."%(t_term))
	except Exception as e:
		return HttpResponse(e, status = 400)

def delete_selected(request):
	try:
		data = req_data(request,True)

		t_term = "Transaction Type"
		terms = get_display_terms(request)
		if terms:
			if terms.transaction_types:
				t_term = terms.transaction_types

		for ids in data['ids']:
			use_in_questions = Assessment_question.objects.filter(company=data['company'],transaction_type=ids,is_active=True).first()
			if use_in_questions:
				raise_error("%s is currently in use."%(use_in_questions.transaction_type.name))
			try:
				record = Exercise.objects.get(pk = ids)
				record.is_active = False
				record.transaction_code = str(record.transaction_code) + str(time.mktime(time.gmtime()))
				record.save()
			except Exercise.DoesNotExist:
				raise_error("%s doesn't exist."%(t_term))
		
		return success("Successfully deleted.")
	except Exception as e:
		return HttpResponse(e,status=400)


def get_intelex_exercises(request):

	try:
		datus 	= req_data(request,True)
		url 	= 'http://35.185.70.123/api/read_exercises/'
		headers = {'content-type': 'application/json'}
		data 	= {"complete_detail": True}

		result 			= requests.post(url, data=json.dumps(data), headers=headers)
		result.encoding = 'ISO-8859-1'
		records 	    = result.json()

		for record in records["records"]:
			cprint(record)
			if Exercise.objects.filter(set_no=record['set_no'], transaction_code__iexact=record['exercise_code'], name__iexact=record['exercise_name'], exercise_id=record['id'], is_intelex=True, is_active=True, company=datus['company']).exists():
				continue
			else:
				datus['transaction_code'] = record['exercise_code']
				datus['name'] 			  = record['exercise_name']
				datus['exercise_id'] 	  = record['id']
				datus['program_id'] 	  = record['program_id']
				datus['is_active'] 		  = True
				datus['is_intelex'] 	  = True
				datus['set_no'] 		  = record['set_no']
				datus['total_items'] 	  = record['total_items']
				datus['company'] 		  = datus['company']

				transaction_type_form = ExerciseForm(datus)

				if(transaction_type_form.is_valid()):
					transaction_type_form.save()
				else:
					return HttpResponse(transaction_type_form.errors, status = 400)
		return HttpResponse("Successfully saved.", status = 200)
		# return HttpResponse("Success", status=200)
	except Exception as e:
		return HttpResponse(e,status=400)
