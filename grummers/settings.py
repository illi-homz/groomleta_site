'''
Django settings for grummers project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
'''

# import dj_database_url
import os
import environ
from pathlib import Path
from datetime import timedelta
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str
import sentry_sdk
from sentry_sdk.integrations.graphene import GrapheneIntegration

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
SENTRY_DSN = env('SENTRY_DSN')
SMSAERO_URL = env('SMSAERO_URL')
SMSAERO_API_KEY = env('SMSAERO_API_KEY')
EMAIL = env('EMAIL')

# DEBUG = False
# DEBUG = True
DEBUG = bool(int(env('IS_DEBUG')))

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'https://grummers-test.herokuapp.com']
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = [
    'http://188.68.220.145',
    'https://groomleta.ru',
    'https://www.groomleta.ru',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
]

INSTALLED_APPS = [
    'django_crontab',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'app',
    'account',
    'django_cleanup.apps.CleanupConfig',
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'grummers.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.abspath(BASE_DIR), '#assets'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'grummers.wsgi.application'


DB_DEV = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DB_PROD = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'grummers_db',
        'USER': 'dbms',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASES = DB_DEV if DEBUG else DB_PROD

# DB_PROD_HEROKU = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}
# DATABASES = DB_PROD_HEROKU

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = False


STATIC_URL = '/staticfiles/'
MEDIA_URL = '/mediafiles/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True
# CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = [
    'http://188.68.220.145',
    'https://groomleta.ru',
    'https://www.groomleta.ru',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://192.168.1.38',
]

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8080',
    'http://localhost:8080',
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'https://groomleta.ru',
    'https://www.groomleta.ru',
]

CORS_ALLOW_ALL_ORIGINS = True

GRAPHENE = {
    'SCHEMA': 'grummers.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=120),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=124),
    'JWT_COOKIE_NAME': 'JWT-Token',
    'JWT_COOKIE_SAMESITE': 'Strict',
    'JWT_CSRF_ROTATION': True,
}

sentry_sdk.init(
    dsn=SENTRY_DSN,
    enable_tracing=True,
    integrations=[
        GrapheneIntegration(),
    ],
)

CRONJOBS = [
    ('0 12 * * *', 'app.cron.run_sms_sender')
]

APP_LOG_FILENAME = os.path.join(BASE_DIR, 'log/app.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s',
        },
        'file': {
            'fomat': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': APP_LOG_FILENAME,
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
    },
}
