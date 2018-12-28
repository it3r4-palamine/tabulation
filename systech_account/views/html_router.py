from django.shortcuts import render
from utils.model_utils import *

def get_dialog_document(request, folder_name, file_name, new):
	try:
		file_location = folder_name + "/dialogs/" + file_name + ".html"

		return_data = {}
		return_data['reference_no'] = code_model_selector(folder_name)

		return render(request, file_location, return_data)
	except Exception as e:
		print e
		return render(request, file_location) 


def get_common_document(request,folder_name,file_name):

	file_location = folder_name + "/" + file_name + ".html"

	return render(request, file_location)