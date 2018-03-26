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

"""WSGI config for ClimbingAssoPortalSite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/

"""

####################################################################################################

import argparse
import os

from django.core.wsgi import get_wsgi_application

####################################################################################################

PROJECT = 'ClimbingAssoPortalSite'

####################################################################################################

parser = argparse.ArgumentParser(
    description='Start WSGI server for {}'.format(PROJECT),
)

parser.add_argument(
    '--mode',
    default='prod',
    help='Mode is dev or prod',
)

args = parser.parse_args()

####################################################################################################

settings_path = PROJECT + '.settings.' + args.mode

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_path)

application = get_wsgi_application()
