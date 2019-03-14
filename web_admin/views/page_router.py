from django.shortcuts import render, redirect


def get_company_sign_up(request):
    return render(request, "login/signup_company.html")


def get_user_selection(request):
    return render(request, "login/landing_user_choice.html")


def get_signin(request):
    return render(request, "login/login_signup.html")


def get_signin_student(request):
    return render(request, "login/sub_pages/student_signin.html")


def get_signin_learning_center(request):
    return render(request, "login/sub_pages/learning_center_signin.html")


def get_login_page(request):
    if request.user.id:
        return redirect("home")
    else:
        return render(request, 'login/landing_page.html')


def get_sign_in_page(request):
    if request.user.id:
        return redirect("home")
    else:
        return render(request, 'login/login.html')


def get_questions_page(request):
    return render(request, "questions/questions.html")


def get_enrollment_page(request):
    return render(request, 'enrollment/enrollment.html')


def get_subjects_page(request):
    return render(request, "subjects/subject.html")


def get_exercise_page(request):
    return render(request, "exercise/exercise.html")



