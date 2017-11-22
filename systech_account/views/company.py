from ..forms.transaction_types import *
from ..models.transaction_types import *
from ..models.company_assessment import *
from ..forms.company import *
from ..models.company import *
from ..views.common import *


def company(request):
	return render(request, 'company/company.html')

def create_dialog(request):
	return render(request, 'company/dialogs/create_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		filters = {}
		filters['is_active'] = True
		# has_transaction = data.get("transaction_type",None)
		# if has_transaction:
		# 	filters['transaction_type'] = has_transaction

		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		records = Company.objects.filter(**filters).order_by("id")
		results = {'data':[]}
		results['total_records'] = records.count()

		if pagination:
			results.update(generate_pagination(pagination,records))
			records = records[results['starting']:results['ending']]
		data = []
		for record in records:
			company_transaction_type = []
			row = record.get_dict()

			if record.transaction_type:
				for t_types in record.transaction_type:
					try:
						t_type = Transaction_type.objects.get(id=t_types,is_active=True)
					except Transaction_type.DoesNotExist:
						continue
					transaction_type_dict = {'id':t_type.pk,'name':t_type.name,'is_active':t_type.is_active}
					company_transaction_type.append(transaction_type_dict)
			row['transaction_type'] = company_transaction_type
			data.append(row)
		results['data'] = data
		return success_list(results,False)
	except Exception as e:
		return HttpResponse(e, status = 400)

def create(request):
	try: 
		postdata = post_data(request)
		if 'transaction_types' not in postdata or not postdata['transaction_types']:
			return error("Transaction Type is required.")

		transaction_types = postdata.pop('transaction_types',[])
		
		company_transaction_type = []
		for transaction_type in transaction_types:
			company_transaction_type.append(transaction_type['id'])

		postdata['transaction_type'] = list_to_string(company_transaction_type)
		try:
			instance = Company.objects.get(id=postdata.get('id',None))
			company = Company_form(postdata, instance=instance)
		except Company.DoesNotExist:
			if not Company.objects.filter(name=postdata['name']).exists():
				company = Company_form(postdata)
			else: return error("Company already exists.")

		if company.is_valid():
			company.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(company.errors, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def delete(request,id = None):
	try:
		has_record = Company_assessment.objects.filter(company=id).first()
		if has_record:
			raise_error("This company is currently in use.")
		try:
			record = Company.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success()
		except Company.DoesNotExist:
			raise_error("Company doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)