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

__all__ = [
    'celery_application',
]

####################################################################################################

print('Load', __name__)

####################################################################################################

try:
    # This will make sure the app is always imported when Django starts
    # so that shared_task will use this app.
    from .CelerySetup import application as celery_application
except ImportError:
    # Handle
    #   ImportError: cannot import name 'Celery'
    from pathlib import Path
    import sys
    command = Path(sys.argv[0]).name
    skip = False
    if command not in (
        'create-postgres-database',
    ):
        raise

