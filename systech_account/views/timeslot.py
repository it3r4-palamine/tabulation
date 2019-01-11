
from ..forms.timeslot import *
from ..views.common import *
from ..models.timeslot import *
from utils.date_handler import *
from utils.model_utils import *
from utils.dict_types import *
from utils.response_handler import *
from utils.view_utils import * 

def save_timeslot(request):
	try:
		data = req_data(request)

		student = data.get("student", None)

		data["student"] = student["id"]

		form = TimeSlotForm(data)

		if form.is_valid():
			print("Pass")
			form.save()
		else:
			print(form.errors)

		return success("Success")
	except Exception as e:
		return error(e)

def read(request):
	try:
		filters = req_data(request)

		results = {}
		records = []

		pagination = filters.pop("pagination",None)

		timeslots = TimeSlot.objects.filter(is_deleted=False)

		for timeslot in timeslots:
			records.append(timeslot.get_dict())

		results.update(generate_pagination(pagination,timeslots))
		records = records[results['starting']:results['ending']]

		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		return error(e)