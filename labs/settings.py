"""
Django settings for labs project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

from os.path import join, dirname, abspath
import os
from decouple import config

BASE_DIR = dirname(dirname(abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(config('DEBUG')))

os.environ['HTTPS'] = config('HTTPS')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'clearcache',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'crispy_forms',
    "crispy_tailwind",
    'rest_framework',
    "whitenoise.runserver_nostatic",
    'whitenoise',
    'robots',

    'api',
    'file_control',
    'presence',
    'assistant'
]

# CORS_REPLACE_HTTPS_REFERER = False
# HOST_SCHEME = "http://"
# SECURE_PROXY_SSL_HEADER = None
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = None
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_FRAME_DENY = False
# SECURE_CONTENT_TYPE_NOSNIFF = False
# SECURE_BROWSER_XSS_FILTER = False
# SESSION_COOKIE_HTTPONLY = False

ROBOTS_USE_SCHEME_IN_HOST = True
ROBOTS_USE_SITEMAP = True
ROBOTS_SITEMAP_URLS = {}
ROBOTS_SITEMAP_VIEW_NAME = None

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = eval(config('COOKIE_AGE'))

SITE_ID = int(config('SITE_ID'))

CRISPY_TEMPLATE_PACK = 'tailwind'

ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login/'  # add login
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/join-class'  # add complete_data

ACCOUNT_EMAIL_VERIFICATION = "none"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': join(BASE_DIR, 'caches'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'labs.urls'

if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config('LAB_EMAIL')
    EMAIL_HOST_PASSWORD = config('LAB_PASSWORD')
    DEFAULT_FROM_EMAIL = config('LAB_EMAIL')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'templates'), join(BASE_DIR, 'templates/accounts')],
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

WSGI_APPLICATION = 'labs.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, config('DB_NAME'))
        # 'NAME': BASE_DIR / 'db.sqlite3',
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

MEDIA_ROOT = join(BASE_DIR, 'media')

STATICFILES_DIRS = [join(BASE_DIR, 'static')]
STATIC_ROOT = join(BASE_DIR, 'static/root')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
