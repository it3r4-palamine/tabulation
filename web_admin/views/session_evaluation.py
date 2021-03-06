from ..forms.session import *
from ..models.company_assessment import *
from utils.date_handler import *
from utils.response_handler import *
from web_admin.views.common import *


def create_dialog(request):
	return render(request, 'session_evaluation/dialogs/create_dialog.html')


def read_student_session(request, session_id):
	try:
		results 			= {}
		student_id 			= None
		firstname, lastname = "", ""
		exercises 			= []
		records 			= []
		filters 			= req_data(request)
		company 			= get_current_company(request)

		pagination = filters.pop("pagination", None)

		if session_id:

			if not filters:
				filters["id"] = session_id
			else:
				filters = format_dates(filters)
				results = []
				filters["is_deleted"] = False
				# add_common_filters(filters)

				sessions = StudentSession.objects.filter(**filters)

				for session in sessions:
					results.append(session.get_dict())

				return success_list(results)

			student_session = StudentSession.objects.filter(**filters).prefetch_related('student_session').first()
			session_exercises = StudentSessionExercise.objects.filter(session_id=student_session.id)

			for exercise in student_session.student_session.all():
				exercises.append(exercise.get_dict(complete_instance=True))

			results = student_session.get_dict(complete_instance=True)
			results['session_exercises'] = exercises

		else:

			search = filters.pop("search","")
			date_from = filters.pop("date_from", None)
			date_to = filters.pop("date_to", None)
			name_search = filters.pop("name","")
			session_timein = filters.pop("session_timein","")
			session_timeout = filters.pop("session_timeout","")

			filters = format_times(filters)
			filters = convert_date_key(filters, "session_date")
			filters = set_id(filters)
			q_filters = Q()

			if search:
				q_filters = Q(student__fullname__icontains=search)

			if session_timein and session_timeout:
				q_filters &= Q(session_timein__range=[session_timein,session_timeout])

			if name_search:

				# If user enters full name pyof students, split string
				# and get first and last element

				words = name_search.split(' ')
				firstname = words[0]
				lastname = words[-1]

			q_filters &= (Q(code__icontains=name_search) | Q(student__first_name__icontains=firstname) | Q(student__last_name__icontains=lastname))
			q_filters &= Q(is_deleted=False) & Q(company=company)

			if student_id:
				q_filters &= Q(student_id=student_id)

			if date_from and date_to:
				dfrom = datetime.strptime(date_from, "%Y-%m-%d")
				dto = datetime.strptime(date_to, "%Y-%m-%d")
				q_filters &= (Q(session_date__range = [dfrom, dto]))

			related = ["student","program"]

			sessions = StudentSession.objects.filter(q_filters).select_related(*related).order_by("-id","-code")[:200]

			for session in sessions:
				records.append(session.get_dict(return_type=DEFAULT))

			if pagination:
				results.update(generate_pagination(pagination,sessions))
				records = records[results['starting']:results['ending']]

			results['records'] = records

		return success_list(results,False)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

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
		records = StudentSession.objects.filter(**filters).order_by("id")
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

def create(request,from_api=False,session=None):
	try:
		result = None
		if not from_api:
			session = req_data(request)

			if 'enrollment_id' in session['program']:
				session['enrollment'] = session['program'].get("enrollment_id", None)
				session['program'] = session['program']['program_id']
			
			session = set_id(session)
			session = format_dates(session)
			session = format_times(session)

		if 'id' in session:
			instance = StudentSession.objects.get(id=session['id'])
			form = StudentSessionForm(session, instance=instance)

			if form.is_valid():
				update_result = form.save()
				session_pk = update_result.pk

				StudentSessionExercise.objects.filter(session=session['id']).delete()

				for exercise in clean_list(session['session_exercises']):

					exercise = set_id(exercise)
					exercise['session'] = update_result.pk
					exercise_form = SessionExerciseForm(exercise)

					if exercise_form.is_valid():
						exercise_form.save()
					else:
						raise_error(exercise_form.errors)

				if from_api:
					response = {
						'status' : True,
						'message' : "Success",
						'code' : session["code"]
					}
					return response

				result = {
					"message": "Saving Session "+session["code"]+" Success!",
					"session_pk": session_pk,
				}
				
				return success_list(result, False)
			else:
				raise ValueError(form.errors)

		session_form = StudentSessionForm(session)

		if session_form.is_valid():

			result = session_form.save()
			session_pk = result.pk

			if result:
				for exercise in clean_list(session['session_exercises']):

					exercise['session'] = result.pk
					exercise = set_id(exercise)

					exercise_form = SessionExerciseForm(exercise)
					if exercise_form.is_valid():
						exercise_form.save()
					else:
						raise ValueError(exercise_form.errors)
		else:
			raise ValueError(session_form.errors)

		if from_api:
			response = {
				'status' : True,
				'message' : "Success",
				'code' : session["code"]
			}
			return response
		
		result = {
			"message": "Saving Session "+session["code"]+" Success!",
			"session_pk": session_pk,
		}
		
		return success_list(result, False)
	except Exception as e:
		if result:
			result.delete()

		if from_api:
			response = {
				'status' : False,
				'message' : str(e)
			}
			return response

		return error(e)


def delete(request, session_id):
	try:
		student_session = StudentSession.objects.get(id=session_id)
		student_session.code = remove_non_numeric_str(str(datetime.now()))
		student_session.is_deleted = True
		student_session.save()

		return success()
	except Exception as e:
		return error(str(e))

		
def check_reference_no(request,isChecked=False):
	try:
		data = req_data(request,True)
		instance = StudentSession.objects.filter(is_deleted=False).last()
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
