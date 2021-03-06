"""
Django settings for root project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# from cloghandler import ConcurrentRotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from .local_settings import *


import paypalrestsdk

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ATpJRFvQhoT_Jj9esCrxoIodM22QtG-qWV8A598_E4CLQnvlKtBQPGAXygPJ_Mif3Yrdiu1LqTcs_z0I",
  "client_secret": "EBUTPt-sXI1jbMnu-FGR2UsXu1p3oPkVT-0jUWK8v6xgVDu8W5xAScdXZoreTIweTrPaZXVg3GiCipWY" })


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ew*32x_+=b-g=4g%)111o2isb+)zn(^$6b#wtq_geuf9fy8@jocc%='
PRECISION = 2
DESIGN_STATE = 1 #1 for default and 2 for inspinia
ENVIRONMENT = env
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'web_admin',
    'web_student',
    'api',
]

#INTERNAL_IPS = ('127.0.0.1','127.0.0.1:9000',)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'web_admin.middleware.user_middleware.UserMiddleware',
]

# MIDDLEWARE = [
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'web_admin.middleware.user_middleware.UserMiddleware',
# ]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

AUTH_USER_MODEL = "web_admin.User"

WSGI_APPLICATION = 'root.wsgi.application'

"""Make a file called 'local_settings.py' in the same folder as 'settings.py' and have this as its contents:

name = "accounting"
user = "YOUR-DATABASE-USERNAME-HERE"
password = "YOUR-DATABASE-PASSWORD-HERE"
host = "localhost"
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST' : host,
        'PORT' : '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'passwordhere'
# EMAIL_HOST_PASSWORD = '5QK3g4tfHMzrS3E4AY6QxMyd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/static/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'web_admin/static/uploads')


ERROR_LEVEL = 'WARNING' # DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
CORS_ORIGIN_ALLOW_ALL = True

if env == "staging":
    DEBUG = False
    ALLOWED_HOSTS = []
elif env == "production":
    DEBUG = False
    ALLOWED_HOSTS = [
        "localhost",
        "yahshuaintelex.com",
        "www.yahshuaintelex.com",
        "https://www.yahshuaintelex.com",
        "https://yahshuaintelex.com",
    ]
else:
    # INSTALLED_APPS += ["debug_toolbar","debug_panel",]
    # MIDDLEWARE_CLASSES += ('debug_panel.middleware.DebugPanelMiddleware',)
    INTERNAL_IPS = ('localhost','127.0.0.1','127.0.0.1:8000','127.0.0.1:9000')
    DEBUG = True
    ALLOWED_HOSTS = ["*"]