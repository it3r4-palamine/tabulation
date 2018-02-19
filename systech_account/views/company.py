from ..forms.transaction_types import *
from ..models.transaction_types import *
from ..models.company_assessment import *
from ..forms.company import *
from ..models.company import *
from ..views.common import *
import requests


def company(request):
	return render(request, 'company/company.html')

def create_dialog(request):
	return render(request, 'company/dialogs/create_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		filters = {}
		filters['is_active'] = True
		filters['company'] = data['company']

		exclude = data.pop("exclude",None)
		# has_transaction = data.get("transaction_type",None)
		# if has_transaction:
		# 	filters['transaction_type'] = has_transaction

		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		records = Company_rename.objects.filter(**filters).order_by("id")
		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]
		datus = []
		for record in records:
			company_transaction_type = []
			row = record.get_dict()

			if record.transaction_type:
				if not exclude:
					for t_types in record.transaction_type:
						try:
							t_type = Transaction_type.objects.get(id=t_types,is_active=True,company=data['company'])
						except Transaction_type.DoesNotExist:
							continue
						transaction_type_dict = {'id':t_type.pk,
												'name':t_type.name,
												'is_active':t_type.is_active,
												'code':t_type.transaction_code,
												'set_no':t_type.set_no,
											}
						company_transaction_type.append(transaction_type_dict)
			row['transaction_type'] = company_transaction_type
			datus.append(row)
		results['data'] = datus
		return success_list(results,False)
	except Exception as e:
		return HttpResponse(e, status = 400)

def create(request):
	try: 
		postdata = req_data(request,True)
		t_term = "Transaction Type"
		c_term = "Company"
		terms = get_display_terms(request)
		if terms:
			if terms.transaction_types:
				t_term = terms.transaction_types

			if terms.company_rename:
				c_term = terms.company_rename
		if 'updated_transaction_types' not in postdata or not postdata['updated_transaction_types']:
			return error("%s is required."%(t_term))

		transaction_types = postdata.pop('updated_transaction_types',[])
		
		company_transaction_type = []
		for transaction_type in transaction_types:
			company_transaction_type.append(transaction_type)

		postdata['transaction_type'] = list_to_string(company_transaction_type)
		try:
			instance = Company_rename.objects.get(id=postdata.get('id',None))
			company = Company_rename_form(postdata, instance=instance)
		except Company_rename.DoesNotExist:
			if not Company_rename.objects.filter(name=postdata['name']).exists():
				company = Company_rename_form(postdata)
			else: return error("%s already exists."%(c_term))

		if company.is_valid():
			company.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(company.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def delete(request,id = None):
	try:
		c_term = "Company"
		terms = get_display_terms(request)
		if terms:
			if terms.company_rename:
				c_term = terms.company_rename
		has_record = Company_assessment.objects.filter(company_rename=id,is_active=True).first()
		if has_record:
			raise_error("This %s is currently in use."%(c_term))
		try:
			record = Company_rename.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success("Successfully deleted.")
		except Company_rename.DoesNotExist:
			raise_error("Company doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)

def get_intelex_subjects(request):
	try:
		datus = req_data(request,True)
		url = 'http://35.196.247.86/api/read_programs/'
		headers = {'content-type': 'application/json'}
		data = {'complete_detail': True}
		result = requests.post(url,data=json.dumps(data),headers=headers)
		result.encoding = 'ISO-8859-1'
		records = result.json()

		for record in records['records']:
			print record
			if Company_rename.objects.filter(name__iexact=record['name'],program_id=record['id'],is_intelex=True,is_active=True,company=datus['company']).exists():
				continue
			else:
				program = {}
				program['program_id'] = record['id']
				program['is_active'] = True
				program['is_intelex'] = True
				program['company'] = datus['company']
				program['name'] = record['name']

				transaction_types = Transaction_type.objects.filter(program_id=record['id'],is_active=True,is_intelex=True)
				transaction_typesArr = []
				for transaction_type in transaction_types:
					transaction_typesArr.append(transaction_type.pk)

				program['transaction_type'] = list_to_string(transaction_typesArr)

				company_rename_form = Company_rename_form(program)

				if company_rename_form.is_valid():
					company_rename_form.save()
				else:
					return HttpResponse(transaction_type_form.errors, status = 400)
		return HttpResponse("Successfully saved.", status = 200)
	except Exception as e:
		return HttpResponse(e,status=400)
