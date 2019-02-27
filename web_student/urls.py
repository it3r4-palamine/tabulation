from django.conf.urls import url

from views.page_router import *

urlpatterns = [
    url(r'^$', get_base),
    url(r'^dashboard/$', get_dashboard),

]
