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
import pathlib
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from SettingsTools import *

####################################################################################################

print('Load ClimbingAssoPortalSite.wsgi')

####################################################################################################

parser = argparse.ArgumentParser(
    description='Start WSGI server for {}'.format(PROJECT),
)

add_mode_option(parser)

args = parser.parse_args()

####################################################################################################

set_DJANGO_SETTINGS_MODULE(args.mode)

#! application = get_wsgi_application()
