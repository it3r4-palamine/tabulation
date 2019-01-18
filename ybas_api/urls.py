from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from ybas_api import views
from ybas_api.viewss import download_data
from ybas_api.controllers import answers, users
from ybas_api.controllers import student

urlpatterns = [
    url(r'^api-auth', views.ObtainAuthToken.as_view()), # Refactor
    url(r'^get-data', views.GetData.as_view()),
    url(r'^sync-assessments', views.SyncAssessments.as_view()),
    url(r'^file-upload/', views.FileUpload.as_view()),
    url(r'^file-upload-ios', views.FileUploadIOS.as_view()),
    url(r'^sync-lesson-update', views.LessonUpdate.as_view()),


    url(r'^get-base64-photo', views.GetBase64Photo.as_view()),
    url(r'^get-photo', views.GetPhoto.as_view()),
    url(r'^get-question-photo', views.GetQuestionPhoto.as_view()),
    url(r'^get-answer-image-photo', views.GetAnswerImagePhoto.as_view()),

    url(r'^get-questions/$', answers.GetQuestionList.as_view()),
    url(r'^get-answers/(?P<question_id>[0-9]+)$', answers.GetAnswers.as_view()),

    url(r'^get-profile/$', users.GetUserProfile.as_view()),

    # YIAS Local
    url(r'^get-company-and-user-type/$', views.Get_company_and_user_types.as_view()),
    url(r'^get-programs-and-exercises/$', download_data.Get_programs_and_exercises.as_view()),
    url(r'^get-users/$', download_data.Get_users.as_view()),
    url(r'^get-settings/$', download_data.Get_settings.as_view()),
    url(r'^get-worksheets/$', download_data.Get_worksheets.as_view()),
    url(r'^get-sessions/$', download_data.Get_sessions.as_view()),

    url(r'^get_student_information/$', student.StudentInfo.as_view()),

    url(r'^get_students/$', student.get_students),
    url(r'^get_students_with_information/$', student.get_students_with_information),

    url(r'^save_student_time_logs/$', student.save_student_time_logs),
]