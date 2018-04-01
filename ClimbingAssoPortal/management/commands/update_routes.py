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

# cf. https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/

####################################################################################################

from django.core.management.base import BaseCommand, CommandError

from ClimbingAssoPortal.core.GoogleApi import RouteSpreadsheet

####################################################################################################

# from oauth2client import tools

# cf. http://oauth2client.readthedocs.io/en/latest/source/oauth2client.tools.html#oauth2client.tools.run_flow
# argument_parser = argparse.ArgumentParser(parents=[tools.argparser])
# flags = argument_parser.parse_args()

####################################################################################################

class Command(BaseCommand):

    help = 'Update routes from Google Sheet'

    ##############################################

    def handle(self, *args, **options):

        route_spreadsheet = RouteSpreadsheet(command=self)
        route_spreadsheet.update(commit=True)

        # try:
        #     pass
        # except Exception:
        #     raise CommandError()

        self.stdout.write(self.style.SUCCESS('Success'))
