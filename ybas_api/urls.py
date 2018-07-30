from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from ybas_api import views
from ybas_api.controllers import answers, users


urlpatterns = [
    url(r'^api-auth', views.ObtainAuthToken.as_view()), # Refactor
    url(r'^get-data', views.GetData.as_view()),
    url(r'^sync-assessments', views.SyncAssessments.as_view()),
    url(r'^file-upload/', views.FileUpload.as_view()),
    url(r'^sync-lesson-update', views.LessonUpdate.as_view()),


    url(r'^get-base64-photo', views.GetBase64Photo.as_view()),
    url(r'^get-photo', views.GetPhoto.as_view()),
    url(r'^get-question-photo', views.GetQuestionPhoto.as_view()),
    url(r'^get-answer-image-photo', views.GetAnswerImagePhoto.as_view()),

    url(r'^get-questions/$', answers.GetQuestionList.as_view()),
    url(r'^get-answers/(?P<question_id>[0-9]+)$', answers.GetAnswers.as_view()),

    url(r'^get-profile/$', users.GetUserProfile.as_view()),
]