from django.shortcuts import render, get_object_or_404


def get_document(request):
	document_url = 'print_forms/session_evaluation.html'
	return render(request, document_url)

def get_enrollment_document(request):
	document_url = 'print_forms/enrollment_confirmation_form_2.html'
	return render(request, document_url)