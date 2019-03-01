from django.conf.urls import url

from views.page_router import *

urlpatterns = [
    url(r'^$', get_base),
    url(r'^dashboard/$', get_dashboard),
    url(r'^session_page/$', get_session_page),
    url(r'^questionnaire/$', get_questionnaire_page),
    url(r'^learning_centers/programs/$', get_learning_center_programs_page),
    url(r'^courses/$', get_courses_page),

]
