"""
Django settings for ArtCon project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import json
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
import pymysql




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("DJANGO_SECRET_KEY")
KAKAO_REST_API_KEY = get_secret("KAKAO_REST_API_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "authpage_app.apps.AuthpageAppConfig",
    "boardpage_app.apps.BoardpageAppConfig",
    "exhibpage_app.apps.ExhibpageAppConfig",
    "mainpage_app.apps.MainpageAppConfig",
    "recompage_app.apps.RecompageAppConfig",
    "searchpage_app.apps.SearchpageAppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap4",
    "django_summernote",
    "django_social_share",
    # "django_elasticsearch_dsl",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ##
    "django_cloudflare.CloudflareMiddleware"
]

CF_HEADER_IP_ENABLED = True

ROOT_URLCONF = "ArtCon.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ArtCon.wsgi.application"

# ELASTICSEARCH_DSL={
#     'default': {
#         'hosts': '127.0.0.1:9200'
#     },
# }

# LOGGING = {
#     'version':1,
#     'disable_existing_loggers': False,
#     "filters": {
#         'simple':{
#             'format': 'velname)s %(message)s'
#         }
#     },
#     'handlers': {
#         'logstash': {
#             'level': 'DEBUG',
#             'class': 'logstash.TCPLogstashHandler',
#             'host': 'localhost',
#             'port': 5959, # Default value: 5959
#             'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
#             'message_type': 'django',  # 'type' field in logstash message. Default value: 'logstash'.
#             'fqdn': False, # Fully qualified domain name. Default value: false.
#             'tags': ['django.request'], # list of tags. Default: None.
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['logstash'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         '': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         }
#     },
# }

MYSQL_CONFIG = get_secret("MYSQL_CONFIG")
pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_CONFIG["NAME"],
        "USER": MYSQL_CONFIG["USER"],
        "PASSWORD": MYSQL_CONFIG["PASSWORD"],
        "HOST": MYSQL_CONFIG["HOST"],
        "PORT": MYSQL_CONFIG["PORT"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "authpage_app.User"
LOGIN_REDIRECT_URL = "/index"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

CSRF_USE_SESSIONS = True
