from ..forms.crud import *
from ..models.crud import *
from ..views.common import *


def home(request):
	return render(request, 'crud/home.html')

def create_dialog(request):
	return render(request, 'crud/dialogs/create_dialog.html')

def read(request):
	try:
		records = Record.objects.all().values("id","name").order_by("id")
		return success_list(records)
	except Exception as e:
		return HttpResponse(e, status = 400)

def create(request):
	try: 
		postdata = post_data(request)
		try:
			instance = Record.objects.get(id=postdata.get('id',None))
			record_form = Record_form(postdata, instance=instance)
		except Record.DoesNotExist:
			record_form = Record_form(postdata)

		if(record_form.is_valid()):
			record_form.save()
			return HttpResponse("Successfully saved.", status = 200)
		else:
			return HttpResponse(err, status = 400)
	except Exception as err:
		return HttpResponse(err, status = 400)

def edit(request,id):
	try:
		record = Record.objects.filter(id = id)
		if record.exists():
			record = record.first()
			return success_obj(row.as_dict())
		else:
			raise_error("This record doesn't exists.")
	except Exception as e:
		return HttpResponse(err, status = 400)

def delete(request,id = None):
	try:
		try:
			record = Record.objects.get(pk = id)
			record.delete()
			return success()
		except Record.DoesNotExist:
			raise_error("Record doesn't exist.")
	except Exception as e:
		return HttpResponse(e, status = 400)



