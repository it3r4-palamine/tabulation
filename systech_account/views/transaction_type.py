from ..forms.transaction_types import *
from ..models.transaction_types import *
from ..models.assessments import *
from ..models.company import *
from ..views.common import *
import sys, traceback, os


def transaction_type(request):
	return render(request, 'transaction_type/transaction_type.html')

def create_dialog(request):
	return render(request, 'transaction_type/dialogs/create_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']
		name_search = data.pop("name","")
		# has_company = data.get("company",None)
		# if has_company:
		# 	try:
		# 		company = Company.objects.get(id=has_company)
		# 		filters['id__in'] = company.transaction_type
		# 	except Company.DoesNotExist:
		# 		raise_error("Company doesn't exist.")

		has_ids = data.get('ids',None)
		if has_ids:
			filters['id__in'] = has_ids
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)

		if name_search:
			filters['name__icontains'] = name_search

		sort_by = generate_sorting(data.pop("sort",None))

		records = Transaction_type.objects.filter(**filters).order_by(*sort_by)
		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]
		data = []
		for record in records:
			row = record.get_dict()
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
		print(sys.exc_traceback.tb_lineno)
		print(filename)
		return HttpResponse(e, status = 400)

def create(request):
	try: 
		postdata = req_data(request,True)
		try:
			instance = Transaction_type.objects.get(company=postdata['company'],id=postdata.get('id',None),is_active=True)
			try:
				check_transaction_type = Transaction_type.objects.get(company=postdata['company'],name__iexact=postdata['name'],is_active=True)
				if check_transaction_type.pk != postdata['id']: 
					return error(check_transaction_type.name + " already exists.")

				transaction_type = Transaction_type_form(postdata, instance=instance)
			except Transaction_type.DoesNotExist:
				transaction_type = Transaction_type_form(postdata, instance=instance)
		except Transaction_type.DoesNotExist:
			try:
				check_transaction_type = Transaction_type.objects.get(company=postdata['company'],name__iexact=postdata['name'],is_active=True)
				return error(check_transaction_type.name + " already exists.")
			except Transaction_type.DoesNotExist:
				transaction_type = Transaction_type_form(postdata)

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
			record = Transaction_type.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success("Successfully deleted.")
		except Transaction_type.DoesNotExist:
			raise_error("%s doesn't exist."%(t_term))
	except Exception as e:
		return HttpResponse(e, status = 400)



