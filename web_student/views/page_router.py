from django.shortcuts import render


def get_base(request):
    return render(request, "common/base.html")

def get_dashboard(request):
    return render(request, "common/test.html")