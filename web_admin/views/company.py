from ..forms.transaction_types import *
from ..models.exercises import *
from ..models.company_assessment import *
from ..forms.company import *
from ..models.company import *
from ..views.common import *
import requests


def company(request):
	if request.user.user_type.name.lower() != "technical":
		return redirect("company_assessment_redirect")
	else:
		return render(request, 'company/company.html')

def create_dialog(request):
	return render(request, 'company/dialogs/create_dialog.html')

def read(request):
	try:
		data 				 = req_data(request,True)
		filters 			 = {}
		filters['is_active'] = True
		filters['company'] 	 = data['company']

		name_search 	   	 = data.pop("name","")

		exclude = data.pop("exclude",None)
		# has_transaction = data.get("transaction_type",None)
		# if has_transaction:
		# 	filters['transaction_type'] = has_transaction

		if name_search:
			filters['name__icontains'] = name_search

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
							t_type = Exercise.objects.get(id=t_types, is_active=True, company=data['company'])
						except Exercise.DoesNotExist:
							continue
						transaction_type_dict = {
												'id'		: t_type.pk,
												'name'		: t_type.name,
												'is_active' : t_type.is_active,
												'code'		: t_type.transaction_code,
												'set_no'	: t_type.set_no,
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
		t_term 	 = "Transaction Type"
		c_term 	 = "Company"
		terms 	 = get_display_terms(request)

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
		hours = postdata.get("hours", 0)

		postdata["hours"]  = timedelta(hours=hours, minutes=0) 
		try:
			instance = Company_rename.objects.get(id=postdata.get('id',None))
			company  = Company_rename_form(postdata, instance=instance)
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


def delete(request, id=None):
	try:
		c_term = "Company"
		terms  = get_display_terms(request)
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
		datus 			= req_data(request,True)
		url 			= 'http://35.185.70.123/api/read_programs/'
		headers 		= {'content-type': 'application/json'}
		data 			= {'complete_detail': True}
		result 			= requests.post(url,data=json.dumps(data),headers=headers)
		result.encoding = 'ISO-8859-1'
		records 		= result.json()

		for record in records['records']:
			has_exists = Company_rename.objects.filter(name__iexact=record['name'],program_id=record['id'],is_active=True,company=datus['company']).first()
			if has_exists:
				t_type 			  = has_exists.transaction_type
				transaction_types = Exercise.objects.filter(program_id=record['id'], is_active=True, is_intelex=True)

				for transaction_type in transaction_types:
					if transaction_type.pk not in t_type:
						t_type.append(transaction_type.pk)

				t_types 					= {}
				t_types['program_id'] 		= record['id']
				t_types['is_active'] 		= True
				t_types['is_intelex'] 		= True
				t_types['company'] 			= datus['company']
				t_types['name'] 			= record['name']
				t_types['transaction_type'] = list_to_string(t_type)

				company_rename_form = Company_rename_form(t_types,instance=has_exists)

				if company_rename_form.is_valid():
					company_rename_form.save()
				else:
					return HttpResponse(company_rename_form.errors, status = 400)
			else:
				program 			  = {}
				program['program_id'] = record['id']
				program['is_active']  = True
				program['is_intelex'] = True
				program['company'] 	  = datus['company']
				program['name'] 	  = record['name']

				transaction_types 	 = Exercise.objects.filter(program_id=record['id'], is_active=True, is_intelex=True)
				transaction_typesArr = []
				for transaction_type in transaction_types:
					transaction_typesArr.append(transaction_type.pk)

				program['transaction_type'] = list_to_string(transaction_typesArr)

				company_rename_form = Company_rename_form(program)

				if company_rename_form.is_valid():
					company_rename_form.save()
				else:
					return HttpResponse(company_rename_form.errors, status = 400)
		return HttpResponse("Successfully saved.", status = 200)
	except Exception as e:
		return HttpResponse(e,status=400)
