from django.conf.urls import url

from web_student.views.page_router import *

urlpatterns = [
    url(r'^$', get_base, ),
    url(r'^dashboard/$', get_dashboard, name="student_portal"),
    url(r'^session_page/$', get_session_page),
    url(r'^questionnaire/$', get_questionnaire_page),
    url(r'^learning_centers/programs/$', get_learning_center_programs_page),
    url(r'^courses/$', get_courses_page),

    url(r'^get_dialog/(?P<folder_name>\w{0,50})/(?P<file_name>\w{0,50})/(?P<new>\w{0,50})$',
        get_dialog_document),
]
