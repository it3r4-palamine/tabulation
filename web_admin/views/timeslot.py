
from ..forms.timeslot import *
from ..views.common import *
from ..models.timeslot import *
from ..models.enrollment import Enrollment
from utils.date_handler import *
from utils.model_utils import *
from utils.dict_types import *
from utils.response_handler import *
from utils.view_utils import * 

def save_timeslot(request):
	try:
		data = req_data(request)

		record_id = data.get("id", None)
		student = data.get("student", None)
		data["student"] = student["id"] if student else None

		if record_id:
			instance = TimeSlot.objects.get(id=record_id)
			form = TimeSlotForm(data,instance=instance)
		else:
			form = TimeSlotForm(data)

		if form.is_valid():
			print("Pass")
			form.save()
		else:
			print(form.errors)
			raise ValueError(form.errors)

		return success("Success")
	except ValueError as e:
		return error(e)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
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

		if pagination:
			results.update(generate_pagination(pagination,timeslots))
			records = records[results['starting']:results['ending']]

		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		return error(e)

def read_student_timeslot(request):
	try:
		data = req_data(request)

		results = {}

		enrollment = Enrollment.objects.get(id=data["enrollment_id"])

		results["timeslot"] = enrollment.timeslot.get_dict() if enrollment.timeslot else None

		return success_list(results, False)
	except Exception as e:
		return error(e)

def delete(request,id):
	try:
		data = req_data(request)

		print(id)
		record = TimeSlot.objects.get(id=id)
		record.delete()

		return success("Success")
	except Exception as e:
		return error(e)

