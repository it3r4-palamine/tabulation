from django.shortcuts import render


def get_company_sign_up(request):
    return render(request, "login/signup_company.html")


def get_user_selection(request):
    return  render(request, "login/landing_user_choice.html")
