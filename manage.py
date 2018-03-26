#! /usr/bin/env python3

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
import sys

####################################################################################################

if __name__ == '__main__':

    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClimbingAssoPortalSite.settings.XXX')

    try:
        DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']
        print('DJANGO_SETTINGS_MODULE is {}'.format(DJANGO_SETTINGS_MODULE))
    except KeyError:
        message = '''
You must define the DJANGO_SETTINGS_MODULE environment variable, either

export DJANGO_SETTINGS_MODULE={0}.settings.dev

export DJANGO_SETTINGS_MODULE={0}.settings.prod
'''
        print(message.format('ClimbingAssoPortalSite'))
        sys.exit(1)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exception:
        raise ImportError("Couldn't import Django") from exception

    execute_from_command_line(sys.argv)
