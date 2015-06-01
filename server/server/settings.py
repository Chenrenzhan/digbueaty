#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
"""
路径介绍
http://my.oschina.net/alazyer/blog/202644
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
print()
print(BASE_DIR)
print(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't04$7vn#$^&%km+$)a1gm3bvzexhx34_2$bzh(&_(jy3t0xhc@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'account',
    'evaluate',
    'market',
    'group',
    'notify',
    'order',
    'store',
    'user_center',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'digbueaty',
        'USER':'root',
        'PASSWORD': 'crz332066279',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/



STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\','/')
static = os.path.join(BASE_DIR, 'static').replace('\\','/')
# print(STATIC_ROOT)
STATIC_URL = '/static/'

#$ python manage.py collectstatic
"""
STATICFILES_DIRS,
加载static文件的目录
"""
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'apps/static').replace('\\','/'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\','/')
MEDIA_URL = '/media/'

print(STATICFILES_DIRS)