from ..forms.transaction_types import *
from ..models.transaction_types import *
from ..forms.company import *
from ..models.company import *
from ..forms.company_assessment import *
from ..models.company_assessment import *
from ..models.assessments import *
from django.db.models import *
from ..views.common import *
import sys, traceback, os


def company_assessment(request):
	return render(request, 'company_assessment/company_assessment.html')

def create_dialog(request):
	return render(request, 'company_assessment/dialogs/create_dialog.html')

def read(request):
	try:
		data = req_data(request,True)
		pagination = None

		if 'pagination' in data:
			pagination = data.pop("pagination",None)
		records = Company_assessment.objects.filter(company=data['company'],is_active=True).order_by("id")
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
		exc_type, exc_obj, exc_tb = sys.exc_info()
		filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(sys.exc_traceback.tb_lineno)
		print(filename)
		return HttpResponse(e,status=400)

def create(request):
	try: 
		postdata = req_data(request,True)
		# postdata['transaction_type'] = postdata['transaction_type']['id']
		postdata['company'] = postdata['company']
		postdata['consultant'] = postdata['consultant']['id']

		term = "Transaction Type"
		terms = get_display_terms(request)
		if terms:
			if terms.transaction_types:
				term = terms.transaction_types
		if 'transaction_types' not in postdata:
			return error("%s is required."%(term))

		transaction_types = postdata.pop('transaction_types',[])

		company_assessment_transaction_type = []
		for transaction_type in transaction_types:
			company_assessment_transaction_type.append(transaction_type['id'])

		postdata['transaction_type'] = list_to_string(company_assessment_transaction_type)
		try:
			instance = Company_assessment.objects.get(id=postdata.get('id',None))
			company_assessment = Company_assessment_form(postdata, instance=instance)
		except Company_assessment.DoesNotExist:
			company_assessment = Company_assessment_form(postdata)

		if company_assessment.is_valid():
			assessment_id = company_assessment.save()
			total_questions = Decimal(0)
			total_answers = Decimal(0)
			for transaction_type in company_assessment_transaction_type:
				questions = Assessment_question.objects.filter(Q(company=postdata['company'],transaction_types__contains=[transaction_type],is_active=True) | Q(company=postdata['company'],transaction_type=transaction_type,is_active=True))
				answers = Assessment_answer.objects.filter(company=postdata['company'],transaction_type=transaction_type,company_assessment=assessment_id.pk)
				total_questions += len(questions)
				total_answers += len(answers)

			if not assessment_id.is_generated:
				if total_questions == total_answers:
					assessment_id.is_complete = True
				else:
					assessment_id.is_complete = False
				assessment_id.save()
			return HttpResponse("Successfully saved.",status=200)
		else:
			return HttpResponse(company_assessment.errors,status=400)
	except Exception as err:
		return HttpResponse(err,status=400)

def delete(request,id = None):
	try:
		try:
			record = Company_assessment.objects.get(pk = id)
			record.is_active = False
			record.save()
			return success()
		except Company_assessment.DoesNotExist:
			raise_error("Company assessment doesn't exist.")
	except Exception as e:
		return HttpResponse(e,status=400)

def check_reference_no(request):
	try:
		data = req_data(request,True)
		instance = Company_assessment.objects.filter(is_active=True,company=data['company']).last()
		if not instance:
			last_char = "000001"
		else:
			ref_no = instance.reference_no
			last_char = ref_no[-1:]
			if last_char.isdigit():
				last_char = str(int(last_char) + 1)
				if len(last_char) == 1:
					last_char = ref_no[:-1] + last_char
				else:
					last_char = ref_no[:-2] + last_char
			else:
				last_char += " - 1"
		return success(last_char)
	except Exception as e:
		return HttpResponse(e,status=400)