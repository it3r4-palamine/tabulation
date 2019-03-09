from django.shortcuts import render


def get_company_sign_up(request):
    return render(request, "login/signup_company.html")
