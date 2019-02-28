from django.shortcuts import render


def get_base(request):
    return render(request, "web_student/common/base.html")


def get_dashboard(request):
    return render(request, "web_student/user/dashboard.html")


def get_session_page(request):
    return render(request, "web_student/sessions/session_list.html")


def get_questionnaire_page(request):
    return render(request, "web_student/questionnaire/questionnaire.html")


def get_learning_center_programs_page(request):
    return render(request, "web_student/learning_centers/center_programs.html")
