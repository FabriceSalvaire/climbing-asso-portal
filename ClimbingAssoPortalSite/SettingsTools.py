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

from pathlib import Path
import importlib.util
import os

####################################################################################################

PROJECT = Path(__file__).parent.name

####################################################################################################

def add_mode_option(parser):

    parser.add_argument(
        '--mode',
        default='prod',
        help='Mode is dev or prod',
    )

####################################################################################################

def settings_module(mode):

    return '.'.join((PROJECT, 'settings', mode))

####################################################################################################

def set_DJANGO_SETTINGS_MODULE(mode):

    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module(mode))

####################################################################################################

def load_settings(mode):

    settings_path = Path(__file__).parent.joinpath('settings', mode + '.py')

    spec = importlib.util.spec_from_file_location(settings_module(mode), settings_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
