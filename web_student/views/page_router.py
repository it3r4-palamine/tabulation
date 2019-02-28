from django.shortcuts import render


def get_base(request):
    return render(request, "common/base.html")


def get_dashboard(request):
    return render(request, "user/dashboard.html")


def get_session_page(request):
    return render(request, "sessions/session_list.html")


def get_learning_center_programs_page(request):
    return render(request, "learning_centers/center_programs.html")
