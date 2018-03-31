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

# import argparse
from datetime import datetime
import logging

# from oauth2client import tools

from django.conf import settings

from ClimbingAssoPortalTools.ClimbingGrade import FrenchGrade
from ClimbingAssoPortalTools.GoogleApi import get_credentials, Spreadsheet

from ..models import Route

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# cf. http://oauth2client.readthedocs.io/en/latest/source/oauth2client.tools.html#oauth2client.tools.run_flow
# argument_parser = argparse.ArgumentParser(parents=[tools.argparser])
# flags = argument_parser.parse_args()

####################################################################################################

class GoogleApiAbc:

    _logger = _module_logger.getChild('GoogleApiAbc')

    ##############################################

    def __init__(self, command=None):

        self._command = command

        credential_dir = settings.GOOGLE_API_CREDENTIAL_DIR
        credential_dir.mkdir(exist_ok=True)

        scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        credential_path = credential_dir.joinpath('sheets.ro.json')
        client_secret_file = credential_dir.joinpath('client_secret.json')

        flags = None

        self.log('Get Google API credentials')
        self._credentials = get_credentials(
            settings.GOOGLE_API_APPLICATION_NAME,
            scopes,
            str(credential_path),
            str(client_secret_file),
            flags
        )

    ##############################################

    @property
    def credentials(self):
        return self._credentials

    ##############################################

    def log(self, message, level='info'):

        if self._command is not None:
            self._command.stdout.write(message)
        else:
            self._logger.log(level, message)

####################################################################################################

class RouteSpreadsheet(GoogleApiAbc):

    COLOURS = (
        'noir',
        'blanc',
        #
        'bleu',
        'vert',
        'rouge',
        #
        'fuchsia',
        'jaune',
        #
        'orange',
        'rose',
        'saumon',
        #
        'marbré rouge&blanc',
    )
    COLOUR_MAP = {colour:i for i, colour in enumerate(COLOURS)}

    _logger = _module_logger.getChild('RouteSpreadsheet')

    ##############################################

    def __init__(self, command=None):

        super().__init__(command)

        spreadsheet_id = settings.GOOGLE_API_ROUTE_SPREADSHEET_ID
        self.log('Request spreadsheet {}'.format(spreadsheet_id))
        self._spreadsheet = Spreadsheet(self.credentials, spreadsheet_id)

    ##############################################

    def update(self, commit=True):

        if commit:
            self.log('Delete routes')
            Route.objects.all().delete()

        rows = self._spreadsheet.get_cells(settings.GOOGLE_API_ROUTE_SHEET)
        routes = []
        # colours = set()
        for row in rows:
            if len(row) == 7:
                line_number, grade, colour, name, comment, opener, date = row
                if grade and grade != 'ENF':
                    _ = FrenchGrade(grade)
                route = Route(
                    line_number=int(line_number),
                    grade=grade,
                    colour=self.COLOUR_MAP[colour],
                    name=name,
                    comment=comment,
                    opener=opener,
                    opening_date=datetime.strptime(date, '%d/%m/%Y'),
                )
                routes.append(route)
                # print(route)
                # if commit:
                #    route.save()
                # colours.add(colour)
            else:
                self.log('SKIPPED: {}'.format(row))
        self.log('Retrieved {} routes'.format(len(routes)))
        if commit:
            Route.objects.bulk_create(routes)

        # print(colours)

####################################################################################################

# data = spreadsheet._get()
# print(json.dumps(data, indent=4))

# sheets = [
#     'Liste des voies',
#     'Statistiques - Textuelles',
#     'Statistiques - Graphique',
#     'Voies démontées 2017/12',
#     'Stat démontage 2017/12',
#     'Data',
#     'Voies à ouvrir',
# ]

# for sheet_title in spreadsheet.sheet_titles():
#     print('\n')
#     print('='*100, '\n')
#     print('Title:', sheet_title)
#     try:
#         rows = spreadsheet.get_cells(sheet_title)
#         for row in rows:
#             print(row)
#     except: # googleapiclient.errors.HttpError
#         pass
