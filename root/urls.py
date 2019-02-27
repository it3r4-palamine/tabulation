from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('web_admin.urls')),
    url(r'student_portal/', include('web_student.urls')),
    url(r'api/', include('api.urls')),


]

