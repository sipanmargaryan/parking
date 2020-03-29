import os
from datetime import timedelta

from .base import *  # noqa

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.str('SECRET_KEY', 'Keep it secret!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV.bool('DEBUG', True)
ENABLE_DEBUG_TOOLBAR = DEBUG and ENV.bool('ENABLE_DEBUG_TOOLBAR', False)

ALLOWED_HOSTS = ENV.list('ALLOWED_HOSTS', [])
INTERNAL_IPS = ENV.list('INTERNAL_IPS', default=('127.0.0.1', ))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'django_celery_results',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'channels',
]

PROJECT_APPS = [
    'core',
    'users',
    'messaging',
]

INSTALLED_APPS.extend(EXTERNAL_APPS + PROJECT_APPS)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'project.routing.application'


API_VERSION = 1

# Redis settings
REDIS_URL = 'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_PATH}'.format(
    REDIS_HOST=ENV.str('REDIS_HOST', '127.0.0.1'),
    REDIS_PORT='6379',
    REDIS_PATH='0',
)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# Celery settings
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_ALWAYS_EAGER = ENV.bool('CELERY_TASK_ALWAYS_EAGER', False)


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': ENV.db_url('DATABASE_URL', default='sqlite://:memory:'),
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REST API settings

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}

# User settings

AUTH_USER_MODEL = 'users.User'


# Site settings

SITE_NAME = ENV.str('SITE_NAME', 'Parking')
CLIENT_DOMAIN = ENV.str('CLIENT_DOMAIN', '127.0.0.1:8000')
URL_SCHEME = ENV.str('URL_SCHEME', 'http')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_COUNTRY = ENV.str('DEFAULT_COUNTRY', 'Armenia')

# Routee sms api setting

ROUTEE_APPLICATION_ID = ENV.str('ROUTEE_APPLICATION_ID')
ROUTEE_APPLICATION_SECRET = ENV.str('ROUTEE_APPLICATION_SECRET')

# Firebase Cloud Messaging
FCM_SERVER_KEY = ENV.str('FCM_SERVER_KEY', None)