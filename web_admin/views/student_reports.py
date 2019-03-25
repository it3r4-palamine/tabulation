from django.db.models import CharField, Value as V
from django.db.models import Q, F
from django.db.models.functions import Concat

from ..models.company_assessment import *
from ..views.common import *


def student_reports(request):
	return render(request, 'student_reports/student_reports.html')


def read_enrollment_report(request):
	try:
		filters = req_data(request,True)
		filters = set_id(filters)
		# filters['student_id__grade_level'] = filters.pop("grade_level", None)
		pagination = filters.pop("pagination", None)
		sort_by = filters.pop("sort", None)
		name_search = filters.pop("name", "")
		program_id = filters.pop("program",None)
		school_id = filters.pop("school",None)
		grade_level_id = filters.pop("grade_level",None)
		results = { "records" : [] }
		records = []

		q_filters = (Q(user__fullname__icontains = name_search))
		if program_id:
			q_filters &= (Q(company_rename_id=program_id))

		if school_id:
			q_filters &= (Q(school__id=school_id))

		# if grade_level_id:
		# 	q_filters &= (Q(student_id__grade_level=grade_level_id))

		enrolled_students = Enrollment.objects.filter(q_filters)\
												.values('user')\
												.annotate(full_name=Concat(F('user__fullname'), V(' '), output_field=CharField()))\
												.order_by('full_name')\
												.distinct()

		records = list(enrolled_students)
		results.update(generate_pagination(pagination, enrolled_students))
		records = records[results['starting']:results['ending']]

		results["student_count"] = len(enrolled_students)
		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		return error(e)
