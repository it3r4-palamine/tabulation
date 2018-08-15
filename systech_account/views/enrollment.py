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


def enrollment(request):
	return render(request, 'enrollment/enrollment.html')

def create_dialog(request):
	return render(request, 'enrollment/dialogs/create_dialog.html')

def read_enrollees(request):
	try:
		filters = get_data(request)
		firstname, lastname = "", ""
		results = { "records": [] }
		records = []
		pagination = None

		# Get Filters
		name_search = filters.pop("name", "")
		student_id = filters.pop("student_id",None)
		program_id = filters.pop("program_id",None)
		date_from = filters.pop("date_from","")
		date_to = filters.pop("date_to","")
		session_start_date = filters.pop("session_start_date","")
		session_end_date = filters.pop("session_end_date","")
		school_id = filters.pop("school_id",None)

		# Bad Code. There should be a boolean variable for pagination.
		if "pagination" in filters:
			pagination = filters.pop("pagination", None)
			sort_by = filters.pop("sort", None)
		
		# Q Filters
		q_filters = (Q(is_active=True) & Q(is_deleted=False))

		if date_from and date_to:
			q_filters &= (Q(enrollment_date__range = [date_to_datetime(date_from), date_to_datetime(date_to)]))
		
		if request.user.is_staff:
			# For Admin or Staff Filters

			if student_id:
				q_filters &= (Q(student__id=student_id['id']))

			if program_id:
				q_filters &= (Q(program__id=program_id['id']))

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

			q_filters &= (Q(code__icontains=name_search) | Q(student__first_name__icontains = firstname) | Q(student__last_name__icontains = lastname))
		else:
			q_filters &= (Q(student = request.user.studentprofile.student.id))

		# Query
		# Use select related to improve query speed.
		related = ["student", "program", "school"]
		programs = Enrollment.objects.filter(q_filters).select_related(*related).order_by("-code")

		for program in programs:
			row = program.get_dict(return_type = FOR_LIST)
			row["payments"] = list(program.get_payments())
			records.append(row)


		if pagination:
			results.update(generate_pagination(pagination, programs))
			records = records[results['starting']:results['ending']]
		
		results["records"] = records

		return success_list(results, False)
	except Exception as e:	
		print e
		# return error_response(request, e, show_line=True)