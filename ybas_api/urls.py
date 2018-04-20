from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from ybas_api import views


urlpatterns = [
    url(r'^api-auth', obtain_auth_token), # Refactor
    url(r'^get-data', views.GetData.as_view()),
    url(r'^sync-assessments', views.SyncAssessments.as_view()),
    
    url(r'^get-photo', views.GetPhoto.as_view()),
    url(r'^get-images2', views.GetImage2.as_view()),
]