"""
Django settings for patronazna_sluzba_project project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# ..\GitHub\TPO\patronazna_sluzba_project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#base for static files
# ..\GitHub\TPO\patronazna_sluzba_project\patronazna_sluzba_project
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# http://stackoverflow.com/questions/4919600/django-project-root-self-discovery
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=@yqq%ow_nzt$^qe3p9jc+fav1=!0h7ri7@u)+h)-eoc5k8h)r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'patronazna_sluzba_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'patronazna_sluzba_project.urls'

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

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'enejsi'
EMAIL_HOST_PASSWORD = 'Bordanje009'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


#   AXES settings
#AXES_COOLOFF_TIME: 24
#AXES_USE_USER_AGENT: True   # Pomeni da drug user iz istega ipja se lahk logina
#AXES_LOGIN_FAILURE_LIMIT: 3     # Po 3 poskusih zafejla

WSGI_APPLICATION = 'patronazna_sluzba_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

# STATIC_JOIN:  ..\GitHub\TPO\patronazna_sluzba_project\patronazna_sluzba_project\static
# FOR: static assets that arent tied to a particular app
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# TEST READY PRINT's FOR OS DIR NAVIGATION
# print("BASE_DIR: ", BASE_DIR)
# print("PROJECT_ROOT: ", PROJECT_ROOT)
# print("STATIC_URL: ", STATIC_URL)
# print("STATIC_JOIN: ", os.path.join(PROJECT_ROOT, 'static'))
