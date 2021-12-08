'''
Created on May 30, 2019

@author: akshay.gupta
'''

import datetime
import os
import sys

from hangroo import conf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_7r@^u$sje&a+^w^p)=do!_hchmc8wue+6@j@bp%xv1g#p9g=%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SILENCED_SYSTEM_CHECKS = ['mysql.E001']

APP_VERSION = "1.0.0"
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    #'material.admin',
    #'material.admin.default',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'knox',
    'auditlog',
    'user',
    'rest',
    'notification',
    'product',
    'inventory',
    'order',
    'webapp',
    'commons',
    'bootstrap4',
    'fa',
    'jquery',
    'social_django',
    'crispy_forms',
    'piwik',
    'django_tables2',
    #'django_celery_beat',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',
                                       'rest_framework.authentication.SessionAuthentication',)
    }

REST_KNOX = {
    'USER_SERIALIZER': 'users.serializers.UserSerializer',
    'TOKEN_TTL':datetime.timedelta(hours=24 * 7)
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'hangroo.urls'

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

WSGI_APPLICATION = 'hangroo.wsgi.application'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if conf.use_sqlite:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': conf.database_name,
            'USER': conf.database_user,
            'PASSWORD': conf.database_password,
            'HOST': conf.database_host,  # Or an IP Address that your DB is hosted on
            'PORT': conf.database_port,
            'OPTIONS': {
                'autocommit': True,
            }
        }
    }

AUTHENTICATION_BACKENDS = (
    "social_core.backends.open_id.OpenIdAuth",
    "social_core.backends.google.GoogleOpenId",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = conf.google_oauth_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = conf.google_oauth_secret
DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M:%S']
LOGIN_URL = '/admin'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = [ 'email']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
#    {
#        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE =  'Asia/Kolkata'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json_formattor': {
            'format': '{"time":"%(asctime)s", "log_level":"%(levelname)s", "file_name":"%(pathname)s", "module_name":"%(name)s","function_name":"%(funcName)s","line":"%(lineno)d","message": "%(message)s"}'
        },
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
        }
    },
    'handlers': {
        'application': {
            'level': conf.log_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/application.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 20,
            'formatter': 'json_formattor',
        },
        'request_handler': {
            'level': conf.log_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/django_request.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 20,
            'formatter': 'json_formattor',
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 20,
            'formatter': 'json_formattor',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': 'DEBUG',
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['application', 'console'],
            'level': conf.log_level,
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': conf.log_level,
            'propagate': True
        },
        'django.server': {
            'handlers': ['error_handler'],
            'level': conf.log_level,
            'propagate': False
        },
        'django.template': {
            'handlers': ['error_handler'],
            'level': conf.log_level,
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['error_handler'],
            'level': conf.log_level,
            'propagate': False
        },
        'django.security': {
            'handlers': ['error_handler'],
            'level': conf.log_level,
            'propagate': False
        },
    }
}

ADMIN_SITE_HEADER = "Hangroo Cafe Admin"
ADMIN_SITE_TITLE = "Hangroo Cafe Admin Portal"
ADMIN_INDEX_TITLE = "Welcome to Hangroo Cafe"



######################## AWS Parameters #####################
AMI_OLDER_THAN_X_DAYS = 10
DB_SNAPSHOTS_OLDER_THAN_X_DAYS = 10
# SUPPORTED_AWS_REGION = "ALL"
SUPPORTED_AWS_REGION = "ap-south-1"

######################## Grafana Creds #####################
grafana_host = ""
grafana_authorization_token = ""

######################## Jenkins Creds #####################
jenkins_url = ''
jenkins_user = ''
jenkins_password = ''

######################## Jira Creds #####################
JIRA_BASE_URL = ''
JIRA_USER = conf.jira_user
JIRA_PASS = conf.jira_pass
JIRA_SRE_PROJECT_KEY = "SP"

BOT_HANDEL = "@hangroo"

# ## email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.thesmartcloud.in'
EMAIL_PORT = 25
EMAIL_FROM = 'noreply@thesmartcloud.in'
EMAIL_SUBJECT_PREFIX = "SMARTCLOUD"
EMAIL_TEMPLATE_DIR = "notification/email_templates"
EMAIL_DEFAULT_RECIPIENTS = ['akshaykumargupta2208@gmail.com', ]

# celery
CELERY_BROKER_URL = conf.redis_endpoint
CELERY_RESULT_BACKEND = conf.redis_endpoint
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TIMEZONE = TIME_ZONE

######################## Analytics ##########################
PIWIK_SITE_ID = 5
PIWIK_URL = "https://analytics.galvosoft.com/"

######################## Stock ##########################
nse_host = "https://www1.nseindia.com"
