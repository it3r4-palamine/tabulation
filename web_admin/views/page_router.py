from django.shortcuts import render


def get_company_sign_up(request):
    return render(request, "login/signup_company.html")


def get_user_selection(request):
    return  render(request, "login/landing_user_choice.html")


def get_signin(request):
    return render(request, "login/login_signup.html")


def get_signin_student(request):
    return render(request, "login/sub_pages/student_signin.html")


def get_signin_learning_center(request):
    return render(request, "login/sub_pages/learning_center_signin.html")
