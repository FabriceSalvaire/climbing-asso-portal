####################################################################################################
#
# Climbing Asso Portal - A Portal for Climbing Club (Association)
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import os

from django.conf import settings

from .base import *

####################################################################################################

print('Load', __name__)

####################################################################################################
#
# Debug
#

# SECURITY WARNING: don't run with debug turned on in production !

DEBUG = True # FOR DEV TEST ONLY !!!

####################################################################################################
#
# Logging
#

### LOGGING = {
###     'version': 1,
###     'disable_existing_loggers': False,
###     'handlers': {
###         'console': {
###             'class': 'logging.StreamHandler',
###         },
###     },
###     'loggers': {
###         'django': {
###             'handlers': ['console'],
###             'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
###         },
###     },
### 
###     # 'handlers': {
###     #     'file': {
###     #         'level': 'DEBUG',
###     #         'class': 'logging.FileHandler',
###     #         'filename': '.../debug.log',
###     #     },
###     # },
###     # 'loggers': {
###     #     'django': {
###     #         'handlers': ['file'],
###     #         'level': 'DEBUG',
###     #         'propagate': True,
###     #     },
###     # },
### }

####################################################################################################
#
# Site
#

SITE_ID = 1

ALLOWED_HOSTS = []

####################################################################################################
#
# Statics
#

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR.joinpath('static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

PRIVATE_MEDIA_URL = '/smedia/'
PRIVATE_MEDIA_ROOT = BASE_DIR.joinpath('smedia')

####################################################################################################
#
# Secret Key
#

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'f10_$cj5d_c@g^sr4v_1k3!*epi0#)-#%_oyxbj!&-%1&vxu15' # FOR DEV TEST ONLY !!!

####################################################################################################
#
# Password validation
#

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [ # FOR DEV TEST ONLY !!!
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
# Database
#

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# https://docs.djangoproject.com/en/2.0/ref/databases/

POSTGRESQL_DESCRIPTION = 'Climbing Asso Portal Database'
POSTGRESQL_LOCAL = 'fr_FR.UTF8'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': str(BASE_DIR.joinpath('db.sqlite3')),
    # },
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'climbing_asso_portal',
        'USER': 'climbing_asso_portal',
        'PASSWORD': 'climbing_asso_portal', # FOR DEV TEST ONLY !!!
    }
}

####################################################################################################
#
# Template
#

JINJA_TEMPLATES['OPTIONS']['auto_reload'] = DEBUG

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
# Email
#

# Log to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

####################################################################################################
#
# Cache
#

# Note: django_select2 don't work with a dummy cache !
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# see also https://github.com/django-pylibmc/django-pylibmc
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'memory_cache',
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#         'LOCATION': '/tmp/memcached.sock',
#     }
# }

####################################################################################################
#
# Celery
#

CELERY_BROKER_URL='pyamqp://guest@localhost//'

# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'django-cache'

####################################################################################################
#
#                                      Applications Settings
#
####################################################################################################

####################################################################################################
#
# Account
#

THEME_CONTACT_EMAIL = 'admin@foo.org'

####################################################################################################
#
# Filer
#


FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': str(MEDIA_ROOT.joinpath('filer')),
                'base_url': MEDIA_URL + 'filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': str(MEDIA_ROOT.joinpath('filer_thumbnails')),
                'base_url': MEDIA_URL + 'filer_thumbnails/',
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': str(PRIVATE_MEDIA_ROOT.joinpath('filer')),
                'base_url': PRIVATE_MEDIA_URL + 'filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': str(PRIVATE_MEDIA_ROOT.joinpath('filer_thumbnails')),
                'base_url': PRIVATE_MEDIA_URL + 'filer_thumbnails/',
            },
        },
    },
}

####################################################################################################
#
#                                          Site Settings
#
####################################################################################################

####################################################################################################
#
# Google API
#

GOOGLE_API_CREDENTIAL_DIR = BASE_DIR.joinpath('.google-api-credentials')
GOOGLE_API_APPLICATION_NAME = 'Climbing Asso Portal'
GOOGLE_API_ROUTE_SPREADSHEET_ID = '1xzzypnm80bUooj8ZPMLhtYEQbZtL89QpIBBNFXn5y90'
GOOGLE_API_ROUTE_SHEET = 'Liste des voies'
