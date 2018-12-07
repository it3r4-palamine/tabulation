from systech_account.models import StudentSession
# from yahshua_intelex.models.trainer import Trainer
# from yahshua_intelex.models.student import Student
# from yahshua_intelex.models.program import Program
import re

STUDENT_MODEL = "Student"
TRAINER_MODEL = "Trainer"


def StringToObject(model_name, get_instance = False, filters = {}):
	model = apps.get_model(app_label='yahshua_intelex', model_name=model_name)
	if get_instance:
		model = model.objects.filter(**filters)
	return model

def get_last_code(model):
	order_by = ["-id"]
	exclude = {'code':''}
	filters = {"is_deleted":False}
	instance = StringToObject(model, get_instance = True, filters = filters).order_by(*order_by).exclude(**exclude).first()

	return instance.code

def get_new_code(code,model):
	try:
		ModelObject = StringToObject(model)

		if not code:
			get_last_code(model)

		while ModelObject.objects.filter(code=code,is_deleted=False).exists():
			code = get_next_ref(code)

		return code
	except Exception as e:
		return "0001"

def get_next_ref(code):
	new_code = int(code) + 1
	return str(new_code).zfill(4)

def get_next_code(model,order_by_field,filters,exclude):

	instance = StringToObject(model, get_instance = True, filters = filters).order_by(*order_by_field).exclude(**exclude).first()
	return increment_code(instance.get_code())

def increment_code(code):
	try:
		if code and re.search('[a-zA-Z]', code):

			alpha_str = " ".join(re.findall("[a-zA-Z]+", code))
			numeric_str = re.sub('.*?([0-9]*)$',r'\1',code)

			len_numeric_padding = len(numeric_str)
			numeric_str = int(numeric_str) + 1
			
			return alpha_str + str(numeric_str).zfill(len_numeric_padding)

		elif code:
			new_code = int(code) + 1
			return str(new_code).zfill(4)
		else:
			raise_error()

	except Exception as e:
		print e
		return "0001"

def code_model_selector(folder_name):

	if folder_name == "session_evaluation":
		order_by = ["-id"]
		exclude = {'code':''}
		filters = {"is_deleted":False}
		model = "StudentSession"
	elif folder_name == "student":
		order_by = ["-id"]
		exclude = {'code':""}
		filters = {"is_deleted":False}
		model = "Student"
	elif folder_name == "trainer":
		order_by = ["-id"]
		exclude = {'code':""}
		filters = {"is_deleted":False}
		model = "Trainer"
	elif folder_name == "enrollment":
		order_by = ["-id"]
		exclude = {'code':""}
		filters = {"is_deleted":False}
		model = "Enrollment"
	else:
		return None

	return get_next_code(model,(order_by),filters,exclude)

def check_replace_ref_code(code):
	try:

		while StudentSession.objects.filter(code=code).exists():
			code = get_next_code("StudentSession",["-id"],{"code": code, "is_deleted": False},{"code":""})

		return code
	except Exception as e:
		return "0000"