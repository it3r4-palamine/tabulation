from ..forms.enrollment import *
import time

from django.db.models import *

from utils.response_handler import *
from ..forms.enrollment import *
from ..forms.payment import *
from ..models.assessments import *
from ..models.company_assessment import *
from ..views.common import *


def create_dialog(request):
	pass
	# return render(request, 'enrollment/dialogs/create_dialog.html')

def get_excess_time(request):
	try:
		result = { "excess_time": 0 }
		data = req_data(request,True)

		enrollments = Enrollment.objects\
									.filter(user=data["student_id"], company_rename=data["program_id"], is_deleted=False)\
									.aggregate(total_session_duration=models.Sum(ExpressionWrapper(F('session_credits'), output_field=DurationField())))

		if enrollments["total_session_duration"]:
			session_list = Enrollment.objects.filter(user=data["student_id"], company_rename_id=data["program_id"])

			total_consumed_time = timedelta(microseconds=0, seconds=0)
			for session in session_list:
				total_consumed_time += session.get_total_session_time()

			if total_consumed_time > enrollments["total_session_duration"]:
				excess_time = total_consumed_time - enrollments["total_session_duration"]
				result["excess_time"] = excess_time.total_seconds()

		return success_list(result, False)
	except Exception as err:
		return error_http_response(err, show_line=True)

def read_enrollment(request,enrollment_id):
	try:
		result = {}
		enrollment = Enrollment.objects.get(id=enrollment_id,is_deleted=False)
		payments = enrollment.get_payments()
		result = enrollment.get_dict()
		result["payments"] = list(payments)

		return success_list(result,False)
	except Exception as e:
		return error(e)

def read_enrollees(request):
	try:
		filters = req_data(request,True)
		firstname, lastname = "", ""
		results = { "records": [] }
		records = []
		pagination = None

		# Get Filters
		search = filters.pop("search", "")
		name_search = filters.pop("name_search", "")
		student_id = filters.pop("student_id",None)
		program_id = filters.pop("program_id",None)
		date_from = filters.pop("date_from","")
		date_to = filters.pop("date_to","")
		session_start_date = filters.pop("session_start_date","")
		session_end_date = filters.pop("session_end_date","")
		school_id = filters.pop("school_id",None)
		name_search = search

		# Bad Code. There should be a boolean variable for pagination.
		if "pagination" in filters:
			pagination = filters.pop("pagination", None)
			sort_by = filters.pop("sort", None)

		if search:
			q_filters = Q(user__fullname__icontains=search) | Q(user__first_name__icontains=search)
		
		# Q Filters
		q_filters = (Q(is_active=True) & Q(is_deleted=False) & Q(company=filters['company']))

		if date_from and date_to:

			dfrom = datetime.strptime(date_from, "%Y-%m-%d")
			dto = datetime.strptime(date_to, "%Y-%m-%d")

			q_filters &= (Q(enrollment_date__range = [dfrom, dto]))
		
		if request.user.is_admin:
			# For Admin or Staff Filters

			if student_id:
				q_filters &= (Q(user__id=student_id['id']))

			if program_id:
				q_filters &= (Q(company_rename__id=program_id['id']))

			if date_from and date_to:
				q_filters &= Q(enrollment_date__range=[date_from,date_to])

			if session_start_date and session_end_date:
				q_filters &= Q(session_start_date__range=[session_start_date,session_end_date])

			if school_id:
				if school_id['name'] == "No School":
					q_filters &= (Q(school=None))
				else:
					q_filters &= (Q(school__id=school_id['id']))

			if name_search:
				words = name_search.split(' ')
				firstname = words[0]
				lastname = words[-1]

			q_filters &= (Q(code__icontains=name_search) | Q(user__fullname__icontains = firstname))
		else:
			q_filters &= (Q(student = request.user.studentprofile.student.id))

		# Query
		# Use select related to improve query speed.
		related = ["user", "company_rename", "school"]

		programs = Enrollment.objects.filter(q_filters).select_related(*related).order_by("-id")
		for program in programs:
			row = program.get_dict(dict_type = DEFAULT)

			if row:
				row["payments"] = list(program.get_payments())

			records.append(row)

		if pagination:
			pagination["limit"] = 30
			results.update(generate_pagination(pagination, programs))
			records = records[results['starting']:results['ending']]
		
		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		print(e)
		return error_response(request, e)


def save_enrollment(request):
	try:
		data = req_data(request,True)
		data = set_id(data)
		data = format_dates(data)
		
		if data.get("session_credits", None) is not None:
			session_credits = data["session_credits"]
			minutes = session_credits.get("minutes", None) if session_credits.get("minutes", None) is not None else 0
			hours = session_credits.get("hours", None) if session_credits.get("hours", None) is not None else 0
			data["session_credits"]  = timedelta(hours=hours, minutes=minutes) 
		else:
			data["session_credits"] = None


		try: 
			instance = Enrollment.objects.get(id=data.get("id", None)) 
			form = Enrollment_form(data, instance=instance) 
		except Enrollment.DoesNotExist:

			if Enrollment.objects.filter(code=data["code"]).exists():
				raise ValueError("Enrollment Code Exists")

			form = Enrollment_form(data) 

		if form.is_valid(): 
			enrollment = form.save()

			if enrollment:
				if len(data["deleted_payments"]) > 0:
					Payment.objects.filter(id__in=data["deleted_payments"]).update(is_deleted=True)

				for payment in clean_list(data['payments']):
					payment = format_dates(payment)
					payment['company'] = data['company']
					if "id" in payment:
						instance = Payment.objects.get(id=payment.get("id", None))
						if instance:
							payment["enrollment"] = enrollment.pk
							payment_form = Payment_form(payment,instance=instance)
					else:
						payment["enrollment"] = enrollment.pk
						payment_form = Payment_form(payment)

					if payment_form.is_valid():
						payment_form.save()
					else:
						raise_error(payment_form.errors)

		else:
			raise ValueError(form.errors)


		result = {
			"message": "Saving Enrollment "+data["code"]+" Success!",
			"enrollment_pk": enrollment.pk,
		}

		return success_list(result, False)

	except ValueError as e:
		return error_http_response(str(e))
	except Exception as e:
		return error_http_response(str(e))

def check_reference_no(request,isChecked=False):
	try:
		data = req_data(request,True)
		instance = Enrollment.objects.filter(company=data['company']).last()
		if not instance:
			ref_no = "000000"
		else:
			ref_no = instance.code

		ref_no_len = len(ref_no)


		ref_no = str(int(ref_no) + 1)
		ref_no = ref_no.zfill(ref_no_len)
		if isChecked:
			return ref_no
		else:
			return success(ref_no)
	except Exception as e:
		return HttpResponse(e,status=400)

def delete_enrollment(request):
	try:
		data = req_data(request,True)

		instance = Enrollment.objects.get(id=data.get("id"), is_deleted=False)
		check_assessment = Company_assessment.objects.filter(is_active=True,company_rename__id=data['company_rename']['id'],date_from__gte=data['session_start_date'],date_to=data['session_end_date']).first()
		
		term  = "Company Assessment"
		terms = get_display_terms(request)

		if terms:
			if terms.company_assessments:
				term = terms.company_assessments

		if check_assessment:
			return error("Used in %s. Please be advised!"%(term))

		instance.code = str(instance.code) + str(time.mktime(time.gmtime()))
		instance.is_deleted = True
		instance.save()
		
		return success("Successfully deleted.")
	except Exception as e:
		return error(e)

def read_sessions_reconcile(request):
	try:
		filters = req_data(request,True)
		results = { "enrolled_sessions" : [] , "unenrolled_sessions" : [] }

		enrolled_sessions = Assessment_session.objects.filter(company_assessment__company_rename__pk=filters["company_rename"]['id'],company_assessment__consultant__pk=filters['user']['id'],is_deleted=False)
		# unenrolled_sessions = StudentSession.objects.filter(student_id=filters["student_id"],enrollment=None,is_deleted=False)
		total_session_time = 0

		data = []
		for session in enrolled_sessions:
			results['enrolled_sessions'].append(session.get_dict())
			# total_session_time += session.get_total_session_time().total_seconds()
			# results["enrolled_sessions"].append(session.get_dict(complete_instance=True))

		# results["enroll_total_session_time"] = format_time_consumed(total_session_time)
		# results["enroll_total_session_time_seconds"] = total_session_time
		
		# total_session_time = 0
		# for session in unenrolled_sessions:
		# 	total_session_time += session.get_total_session_time().total_seconds()
		# 	results["unenrolled_sessions"].append(session.get_dict(True))

		# results["non_enroll_total_session_time"] = format_time_consumed(total_session_time)
		# results["non_enroll_total_session_time_seconds"] = total_session_time

		return success_list(results,False)
	except Exception as e:	
		return error(e)

def session_handler_dialog(request):
	return render(request, 'enrollment/dialogs/session_handler_dialog.html')