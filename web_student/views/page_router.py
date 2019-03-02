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


def get_courses_page(request):
    return render(request, "web_student/courses/course_list.html")


def get_dialog_document(request, folder_name, file_name, new):
    try:
        file_location = "web_student/" + folder_name + "/dialogs/" + file_name + ".html"

        return_data = {}

        return render(request, file_location, return_data)
    except Exception:
        return render(request, file_location)
