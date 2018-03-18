# -*- mode: Python -*-

####################################################################################################

"""Django settings for AdhesionSite project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/

"""

####################################################################################################

import os

from django.conf import settings
# from django_jinja.builtins import DEFAULT_EXTENSIONS

####################################################################################################
#
# Debug
#

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

####################################################################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

####################################################################################################

ROOT_URLCONF = 'AdhesionSite.urls'

WSGI_APPLICATION = 'AdhesionSite.wsgi.application'

SITE_ID = 1

ALLOWED_HOSTS = []

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#v2=-7xr3=5(^63sc4)374j48j-d23bo4gc%z$+a#nji56k%we'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

####################################################################################################
#
# Database
#

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

####################################################################################################
#
# Application definition
#

INSTALLED_APPS = [
    # /!\ ordered list
    'suit', # must be added before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'django_jinja', # http://niwinz.github.io/django-jinja/latest/
    'bootstrapform', # https://github.com/tzangms/django-bootstrap-form

    # 'pinax_theme_bootstrap', # https://github.com/pinax/pinax-theme-bootstrap
    'account', # http://django-user-accounts.readthedocs.io/en/latest

    # https://django-filer.readthedocs.io
    'easy_thumbnails',
    'filer',
    'mptt',

    'AdhesionApplication',

    # https://github.com/applecat/django-simple-poll
    # https://github.com/byteweaver/django-polls
    # https://github.com/hmtanbir/django-easy-poll
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'account.middleware.ExpiredPasswordMiddleware',
]

####################################################################################################
#
# Template
#

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        # 'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True, # looks for app/jinja2
        'OPTIONS': {
            "app_dirname": "jinja2",
            # 'match_extension': '.jinja',
            # 'match_extension': '.html',
            'match_extension': None,
            'match_regex': r"^(?!admin/).*", # \.(html|txt)$

            'newstyle_gettext': True,

            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'account.context_processors.account',
                'AdhesionApplication.context_processors.site',
            ],

            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                'jinja2.ext.with_',
                'jinja2.ext.i18n',
                'jinja2.ext.autoescape',
                'django_jinja.builtins.extensions.CsrfExtension',
                'django_jinja.builtins.extensions.CacheExtension',
                'django_jinja.builtins.extensions.TimezoneExtension',
                'django_jinja.builtins.extensions.UrlsExtension',
                'django_jinja.builtins.extensions.StaticFilesExtension',
                'django_jinja.builtins.extensions.DjangoFiltersExtension',
            ],

            'bytecode_cache': {
                'name': 'default',
                'backend': 'django_jinja.cache.BytecodeCache',
                'enabled': False,
            },
            'autoescape': True,
            'auto_reload': settings.DEBUG,
            'translation_engine': 'django.utils.translation',
            "globals": {
                # 'urlnext': 'AdhesionApplication.JinjaExtension.account',
            },
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [
            'filer/templates',
            'AdhesionApplication/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'account.context_processors.account',
                # 'pinax_theme_bootstrap.context_processors.theme',
            ],
        },
    },
]

####################################################################################################
#
# Password validation
#

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

# Fixme: Not in production !
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

####################################################################################################
#
# Internationalization
#

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

####################################################################################################
#
# Django Suit configuration
#

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'AdhesionApplication DB',
    'HEADER_DATE_FORMAT': 'l, j F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,

    'LIST_PER_PAGE': 15
}

####################################################################################################
#
# REST Framework
#

####################################################################################################
#
# Email
#

# Log to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

####################################################################################################
#
# Account
#

ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_DELETION_MARK_CALLBACK = None # Fixme:
THEME_CONTACT_EMAIL = 'admin@foo.org'

####################################################################################################
#
# Easy Thumbail
#

# THUMBNAIL_PROCESSORS = (
#     'easy_thumbnails.processors.colorspace',
#     'easy_thumbnails.processors.autocrop',
#     #'easy_thumbnails.processors.scale_and_crop',
#     'filer.thumbnail_processors.scale_and_crop_with_subject_location',
#     'easy_thumbnails.processors.filters',
# )

####################################################################################################
#
# Filer
#

# FILER_CANONICAL_URL = 'sharing/'
