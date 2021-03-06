"""
Django settings for AppraisalSystem project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
sys.path.append("..")
from settings import MSSQL_SETTINGS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's#$=sm%g=^(-6k04-8^r%q0kdw19+g^3qzofg^nl^74=r(u+d)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'plots',
    # 'mytest',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'AppraisalSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates',
                 # os.path.join(BASE_DIR, 'mytest/templates'),
                 os.path.join(BASE_DIR, 'plots/templates')],
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

WSGI_APPLICATION = 'AppraisalSystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.sqlite3',
#         # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
#         'NAME': 'appraisal',  # 数据库名，先前创建的
#         'USER': 'root',  # 用户名，可以自己创建用户
#         'PASSWORD': '00000',  # 密码
#         'HOST': 'localhost',  # mysql服务所在的主机ip
#         'PORT': '3306',  # mysql服务端口
#     }
# }

# DATABASES = {
#     'default': {
#
#         'ENGINE' : 'sql_server.pyodbc',
#         'NAME' : 'ecology',
#         'HOST' : 'localhost',
#         'PORT' : 1433,
#         'USER' : 'sa',
#         'PASSWORD' : 'Do8gjas07gaS1',
#         'OPTIONS': {
#             'DRIVER': 'SQL Server',
#         },
#     }
# }

DATABASES = {
    'default': {

        'ENGINE' : 'sql_server.pyodbc',
        'NAME' : MSSQL_SETTINGS.NAME,
        'HOST' : MSSQL_SETTINGS.HOST,
        'PORT' : MSSQL_SETTINGS.PORT,
        'USER' : MSSQL_SETTINGS.USER,
        'PASSWORD' : MSSQL_SETTINGS.PASSWORD,
        'OPTIONS': {
            'DRIVER': MSSQL_SETTINGS.DRIVER,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = '/plots'
LOGOUT_REDIRECT_URL = ''


STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static/'),
)

