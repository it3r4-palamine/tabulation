from utils.response_handler import *
from ..models.enrollment import * 

def read_enrolled_programs(request, from_api = False, has_user=True):
	try:
		filters = get_data(request)
		results = { "records" : [] }

		if has_user:
			q_filters = Q(user=filters["id"]) & ~Q(session_end_date__lte=datetime.now()) & Q(is_deleted=False)
		else:
			q_filters = ~Q(session_end_date__lte=datetime.now()) & Q(is_deleted=False)


		if from_api:
			q_filters = ~Q(session_end_date__lte=datetime.now()) & Q(is_deleted=False)

		enrolled_program = Enrollment.objects.filter(q_filters).order_by("company_rename__name")

		for program in enrolled_program:
			credits = program.get_remaining_credit()
			if (credits / 60) > 1:

				if not has_user:
					row = program.get_dict_as_program()
					row["student"] = program.user.get_dict()
				else:
					row = program.get_dict_as_program()

				results["records"].append(row)

		if len(results["records"]) == 0:
			raise_error("No Enrolled Programs available, No more Session credits, or Enrollment Expired")

		if from_api:
			return results

		return success_list(results,False)
	except Exception as err:

		if from_api:
			return {}

		return error_http_response(err)