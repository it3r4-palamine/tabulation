from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'', include('systech_account.urls')),
    url(r'api/', include('ybas_api.urls')),
]
