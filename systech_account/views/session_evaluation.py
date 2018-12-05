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

def session_evaluation_list(request):
	return render(request, "session_evaluation/session_evaluation_list.html", {"pagename" : "Student Evaluation"})

def create_dialog(request):
	return render(request, 'session_evaluation/dialogs/create_dialog.html')
	
def read_student_session(request, session_id):
	try:
		student_id = None
		firstname, lastname = "", ""
		results = {}
		exercises = []
		records = []
		filters = get_data(request)

		pagination = filters.pop("pagination",None)
		sort_by = filters.pop("sort",None)

		if session_id:

			if not filters:
				filters["id"] = session_id
			else:
				filters = format_dates(filters)
				results = []
				add_common_filters(filters)

				sessions = StudentSession.objects.filter(**filters)

				for session in sessions:
					results.append(session.get_dict())

				return success_list(results)

			student_session = StudentSession.objects.filter(**filters).prefetch_related('student_session').first()
			session_exercises = SessionExercise.objects.filter(session_id=student_session.id)

			for exercise in student_session.student_session.all():
				exercises.append(exercise.get_dict(complete_instance=True))

			results = student_session.get_dict(complete_instance=True)
			results['session_exercises'] = exercises

		else:
			if not request.user.is_staff:
				student_id = request.user.studentprofile.student.id
				

			name_search = filters.pop("name","")
			session_timein = filters.pop("session_timein","")
			session_timeout = filters.pop("session_timeout","")

			filters = format_times(filters)
			filters = convert_date_key(filters, "session_date")
			filters = set_id(filters)
			filters = filter_obj_to_q(filters)

			if session_timein and session_timeout:
				filters &= Q(session_timein__range=[session_timein,session_timeout])

			if name_search:

				# If user enters full name of students, split string
				# and get first and last element

				words = name_search.split(' ')
				firstname = words[0]
				lastname = words[-1]

			filters &= (Q(code__icontains=name_search) | Q(student__first_name__icontains=firstname) | Q(student__last_name__icontains=lastname))
			filters &= Q(is_deleted=False)

			if student_id:
				filters &= Q(student_id=student_id)

			related = ["student","program"]
			sessions = StudentSession.objects.filter(filters).select_related(*related).order_by("-id","-code")

			for session in sessions:
				records.append(session.get_dict(return_type=FOR_LIST))

			if pagination:
				results.update(generate_pagination(pagination,sessions))
				records = records[results['starting']:results['ending']]

			results['records'] = records


		return success_list(results,False)
	except Exception as e:
		return error(e)

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
							t_type = Transaction_type.objects.get(id=t_types,is_active=True,company=data['company'])
						except Transaction_type.DoesNotExist:
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
		
def check_reference_no(request,isChecked=False):
	try:
		data = req_data(request,True)
		instance = Company_assessment.objects.filter(company=data['company']).last()
		if not instance:
			ref_no = "000000"
		else:
			ref_no = instance.reference_no

		ref_no_len = len(ref_no)


		ref_no = str(int(ref_no) + 1)
		ref_no = ref_no.zfill(ref_no_len)
		if isChecked:
			return ref_no
		else:
			return success(ref_no)
	except Exception as e:
		return HttpResponse(e,status=400)
