from utils.response_handler import *
from ..forms.form_subject import *
from ..views.common import *


def create(request):
	try:
		data = req_data(request)

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
		company = get_current_company(request)

		subjects = Subject.objects.filter(company=company, is_deleted=False)

		for subject in subjects:
			records.append(subject.get_dict())

		results["records"] = records

		return success_list(results, False)
	except Exception as e:
		return error(str(e))