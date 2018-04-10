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

"""Django settings for Climbing Asso Portal project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/

"""

####################################################################################################

from pathlib import Path

# from django_jinja.builtins import DEFAULT_EXTENSIONS

####################################################################################################

print('Load', __name__)

####################################################################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parents[2]

####################################################################################################

ROOT_URLCONF = 'ClimbingAssoPortalSite.urls'

WSGI_APPLICATION = 'ClimbingAssoPortalSite.wsgi.application'

####################################################################################################
#
# Application definition
#

INSTALLED_APPS = [
    # /!\ ordered list
    'suit', # must be added before admin
    # 'ClimbingAssoPortal.apps.SuitConfig', # custom suit v2 config
    # http://django-suit.readthedocs.io/en/develop
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis', # https://docs.djangoproject.com/en/2.0/ref/contrib/gis/

    'django.contrib.sites',

    'rest_framework', # http://www.django-rest-framework.org
    'django_filters', # https://django-filter.readthedocs.io/en/latest
    'rest_framework_gis', # https://github.com/djangonauts/django-rest-framework-gis
    'rest_framework_swagger', # https://django-rest-swagger.readthedocs.io/en/latest
    'drf_yasg', # https://drf-yasg.readthedocs.io/en/stable/

    # used by DRF filter
    'crispy_forms', # http://django-crispy-forms.readthedocs.io/en/latest/

    'reversion', # https://django-reversion.readthedocs.io/en/stable

    'django_jinja', # http://niwinz.github.io/django-jinja/latest
    'bootstrapform', # https://github.com/tzangms/django-bootstrap-form

    'django_select2', # http://django-select2.readthedocs.io/en/latest

    # 'pinax_theme_bootstrap', # https://github.com/pinax/pinax-theme-bootstrap
    'account', # http://django-user-accounts.readthedocs.io/en/latest

    # https://django-filer.readthedocs.io
    'easy_thumbnails',
    'filer',
    'mptt',

     # http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django
    'django_celery_results', # http://django-celery-results.readthedocs.io/en/latest/
    'django_celery_beat', # http://django-celery-beat.readthedocs.io/en/latest/

    'health_check', # http://django-health-check.readthedocs.io/en/latest/index.html
    'health_check.db',             # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    # 'health_check.contrib.celery', # requires celery
    'health_check.contrib.psutil', # disk and memory utilization; requires psutil

    'graphene_django', # http://docs.graphene-python.org/projects/django/en/latest

    'ClimbingAssoPortal.apps.ClimbingAssoPortalConfig',

    # https://github.com/applecat/django-simple-poll
    # https://github.com/byteweaver/django-polls
    # https://github.com/hmtanbir/django-easy-poll
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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

JINJA_TEMPLATES = {
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
            'ClimbingAssoPortal.context_processors.site',
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

            'ClimbingAssoPortal.jinja_extensions.i18n.DjangoI18n',
        ],

        'bytecode_cache': {
            'name': 'default',
            'backend': 'django_jinja.cache.BytecodeCache',
            'enabled': False,
        },
        'autoescape': True,
        'auto_reload': False, # reset in super
        'translation_engine': 'django.utils.translation',
        "globals": {
            # 'urlnext': 'ClimbingAssoPortal.JinjaExtension.account',
        },
    },
}

DJANGO_TEMPLATES = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    # 'DIRS': [],
    'DIRS': [
        'filer/templates',
        'ClimbingAssoPortal/templates',
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
}

TEMPLATES = [
    JINJA_TEMPLATES,
    DJANGO_TEMPLATES,
]

####################################################################################################
#
#                                      Applications Settings
#
####################################################################################################

####################################################################################################
#
# Django Suit configuration
#

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Climbing Asso Portal',
    'HEADER_DATE_FORMAT': 'l, j F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,

    'LIST_PER_PAGE': 20,
}

####################################################################################################
#
# REST Framework
#

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',

    # http://www.django-rest-framework.org/api-guide/permissions/
    'DEFAULT_PERMISSION_CLASSES': (
        # DjangoModelPermissionsOrAnonReadOnly
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),

    'PAGE_SIZE': 100,
}

# cf. https://django-rest-swagger.readthedocs.io/en/latest/settings/
SWAGGER_SETTINGS = {
}

####################################################################################################
#
# Account
#

# http://django-user-accounts.readthedocs.io/en/latest/usage.html#using-email-address-for-authentication
# ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_DELETION_MARK_CALLBACK = None # Fixme:

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

# FILER_ENABLE_PERMISSIONS = False
# Activate the or not the Permission check on the files and folders before displaying them in the
# admin. When set to False it gives all the authorization to staff members based on standard Django
# model permissions.

# FILER_IS_PUBLIC_DEFAULT = True
# Should newly uploaded files have permission checking disabled (be public) by default.

# FILER_STORAGES
# A dictionary to configure storage backends used for file storage.

# FILER_PAGINATE_BY = 20
# The number of items (Folders, Files) that should be displayed per page in admin.

# FILER_SUBJECT_LOCATION_IMAGE_DEBUG = False
# Draws a red circle around to point in the image that was used to do the subject location aware
# image cropping.

# FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = False
# Regular users are not allowed to create new folders at the root level, only subfolders of already
# existing folders, unless this setting is set to True.

# FILER_IMAGE_MODEL = False
# Defines the dotted path to a custom Image model; please include the model name. Example:
# ‘my.app.models.CustomImage’

# FILER_CANONICAL_URL = 'canonical/'
# Defines the path element common to all canonical file URLs.

# FILER_UPLOADER_CONNECTIONS = 3
# Number of simultaneous AJAX uploads. Defaults to 3.

####################################################################################################
#
# Graphene
#

GRAPHENE = {
    'SCHEMA': 'ClimbingAssoPortal.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ]
}

####################################################################################################
#
# Health Check
#

 # to prevent DOS attack on health url, use make_secret
HEALTH_CHECK_URL_KEY = 'dev-only'

HEALTH_CHECK = {
    'DISK_USAGE_MAX': 90, # %
    'MEMORY_MIN': 100,    # MB
}
