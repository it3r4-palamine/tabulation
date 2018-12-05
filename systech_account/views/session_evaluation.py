from ..views.common import *

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
