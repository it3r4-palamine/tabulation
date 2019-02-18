from utils.view_utils import *
from utils.date_handler import *
from ..models import *
from ..models import Enrollment, StudentSession
from utils.global_variables import *
from ..views.program import *

def read_student_status(request):
	try:

		DATE_TODAY = datetime.now()

		results = {
			'count_enrolled_students': 0
		}

		filters = {
			'enrollment_date__month': DATE_TODAY.month,
			'enrollment_date__year' : DATE_TODAY.year,
			'is_deleted' : False,
		}

		count_enrolled_students = Enrollment.objects.filter(**filters).count()
		count_enrolled_total = Enrollment.objects.filter(is_deleted=False).count()
		count_enrolled_by_school = Enrollment.objects\
										.filter(is_deleted=False)\
										.values("school")\
										.annotate(student_count=Count('*'),school_name=F("school__name")).order_by()

		results["count_enrolled_students"] = count_enrolled_students
		results["count_enrolled_total"] = count_enrolled_total
		results["count_enrolled_by_school"] = list(count_enrolled_by_school)

		return success_list(results,False)
	except Exception as e:
		return error(e)

def read_monthly_students_enrolled(request):
	try:
		DATE_TODAY = datetime.now()

		months = [
			'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12' 
		]

		month_names = [
			'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
		]

		final_data = []
		results = {'data':[]}

		for x, month in enumerate(months):
			enrollees = Enrollment.objects.filter(Q(enrollment_date__month=month,enrollment_date__year=DATE_TODAY.year) |
										Q(session_start_date__month=month,session_start_date__year=DATE_TODAY.year)).values("school","is_deleted")\
										.annotate(student_count=Count('*')).order_by()

			enrolled = 0
			inactive = 0
			row = {}
			row['month'] = month_names[x]
			row['students'] = enrolled
			row['inactive'] = inactive
			for enrollee in enrollees:
				if enrollee['is_deleted'] == False:
					enrolled += enrollee['student_count']
					row['students'] = enrolled
				else:
					inactive += enrollee['student_count']
					row['inactive'] = inactive

			final_data.append(row)

		results['data'] = final_data
		return success(results)
	except Exception as e:
		return error(e)

def read_sessions_status(request):
	try:
		DATE_TODAY = datetime.now()
		
		previous_month = DATE_TODAY.month - 1
		
		results = {
			'count_sessions_created': 0,
			'expiring_enrollments': [],
			'expiring_sessions' : [],
			'depleting_credits' : []
		}

		
		filters = {
			'session_date__month': DATE_TODAY.month,
			'session_date__year' : DATE_TODAY.year,
			'is_deleted' : False,
		}

		count_sessions_created = StudentSession.objects.filter(**filters).count()
		count_sessions_total = StudentSession.objects.filter(is_deleted=False).count()
		count_unaccounted_sessions = StudentSession.objects.filter(is_deleted=False,enrollment=None).count()
		count_sessions_daily = StudentSession.objects.filter(session_date=DATE_TODAY,is_deleted=False).count()
		count_sessions_last_month = StudentSession.objects.filter(session_date__month=previous_month,is_deleted=False).count()
		student_session_list = StudentSession.objects.filter(is_deleted=False).values('student',).annotate(session_count=Count('student'),full_name=F('student__first_name')).order_by('-session_count')[:10]
		expiring_enrollments = Enrollment.objects.filter(session_end_date__gte=datetime.now(),session_end_date__lte=datetime.now()+timedelta(days=10),is_deleted=False).order_by('session_end_date')
		expiring_sessions = StudentSession.objects.filter(session_date=datetime.now(),is_deleted=False).order_by("session_timeout")
		depleting_enrollment = Enrollment.objects.filter(session_end_date__gte=datetime.now(),is_deleted=False)

		for enrollment in depleting_enrollment:
			seconds = enrollment.get_remaining_credit()

			if seconds <= 36000:
				row = enrollment.get_dict()
				row["remaining_credit"] = seconds
				results["depleting_credits"].append(row)

		for session in expiring_sessions:
			results["expiring_sessions"].append(session.get_dict())

		for enrollment in expiring_enrollments:

			if enrollment.session_end_date:
				remaining_days = enrollment.session_end_date - date.today()

			remaining_credit = enrollment.get_remaining_credit()

			row = enrollment.get_dict()
			row["remaining_days"] = remaining_days.days
			row["remaining_credit"] = remaining_credit

			results["expiring_enrollments"].append(row)

		results["count_sessions_created"] = count_sessions_created
		results["count_sessions_created"] = count_sessions_created
		results["count_sessions_total"] = count_sessions_total
		results["count_sessions_daily"] = count_sessions_daily
		results["count_sessions_last_month"] = count_sessions_last_month
		results["count_unaccounted_sessions"] = count_unaccounted_sessions
		results["student_session_list"] = list(student_session_list)

		return success_list(results,False)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print(str(e))
		return error(e)

def read_monthly_session_created(request):
	try:
		months = [
			'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12' 
		]

		month_names = [
			'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
		]

		final_data = []
		results = {'data':[]}


		for x, month in enumerate(months):
			filters = {
				'session_date__month': month,
				'session_date__year' : DATE_TODAY.year,
			}
			sessions_created = StudentSession.objects.filter(**filters)

			created = 0
			inactive = 0
			row = {}
			row['month'] = month_names[x]
			row['created'] = created
			row['inactive'] = inactive

			for session_created in sessions_created:
				if session_created.is_deleted == False:
					created += 1
					row['created'] = created
				else:
					inactive += 1
					row['inactive'] = inactive

			final_data.append(row)

		results['data'] = final_data
		return success_list(results,False)
	except Exception as e:
		return error(e)

def read_student_birthdate(request):
	try:
		i = datetime.today()
		date_month = i.strftime('%m')

		results = {'data' : []}

		students = Student.objects.filter(is_active=True,is_deleted=False,date_of_birth__month=date_month).order_by("date_of_birth")
		
		data = []
		for student in students:
			row = student.get_dict()

			data.append(row)

		results['data'] = data
		return success_list(results,False)

	except Exception as e:
		return error(e)


def unenrolled_sessions_graph(request):
	try:
		result = {
			"graph_data": [],
			"session_list": [],
		}
		graph_data = []
		session_list = []
		# q_filters = (Q(enrollment=None) & Q(session_date__year = DATE_TODAY.year))
		values = (
			"student", "program", "evaluated_by", "session_date", "is_deleted"
		)

		for month in months:
			# if month["no"] > DATE_TODAY.month: break

			# q_filters &= Q(session_date__month = month["no"])

			sessions_qs = StudentSession.objects.filter(enrollment=None, session_date__month=month["no"], session_date__year=DATE_TODAY.year).order_by("session_date")

			session_count = 0
			inactive_session_count = 0

			data = {
				"month": month["name"],
				"session_count": session_count,
				"inactive_session_count": inactive_session_count,
			}

			for session in sessions_qs:
				if not session.is_deleted:
					session_count += 1
					session_list.append(session.get_dict())
				else: inactive_session_count += 1

			data["session_count"] = session_count
			data["inactive_session_count"] = inactive_session_count

			graph_data.append(data)

		session_list.sort()

		result["graph_data"] = graph_data
		result["session_list"] = session_list
		return success(result)
	except Exception as e:
		return error(e)

def read_timeslot_summary(request):
	try:

		enrolled_students_active = read_enrolled_programs(request, from_api=True, has_user=False)
		print('=====================')
		print(enrolled_students_active)
		print('=====================')

		for enrolled_student in enrolled_students_active["records"]:
			print(enrolled_student)


		results = { "records" : enrolled_students_active["records"] }


		return success_list(results, False)
	except Exception as e:
		return error(e)