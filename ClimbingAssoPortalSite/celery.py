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
#
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
#
####################################################################################################

####################################################################################################

import os

from celery import Celery

####################################################################################################

PROJECT = 'ClimbingAssoPortalSite'

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', PROJECT + '.settings')

application = Celery(PROJECT)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
application.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
application.autodiscover_tasks()

@application.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
