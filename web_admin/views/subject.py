from ..forms.form_subject import *
from ..views.common import *
from ..models.timeslot import *
from ..models.enrollment import Enrollment
from utils.date_handler import *
from utils.model_utils import *
from utils.dict_types import *
from utils.response_handler import *
from utils.view_utils import * 


def create(request):
	try:
		data = req_data(request)

		print(data)

		form = SubjectForm(data)

		if form.is_valid():
			form.save()
		else:
			raise_error(form.errors) 

		return success("Success")
	except Exception as e:
		return error(str(e))

def read(request):
	try:
		results = {}
		records = []

		subjects = Subject.objects.filter()

		for subject in subjects:
			records.append(subject.get_dict())

		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		return error(str(e))