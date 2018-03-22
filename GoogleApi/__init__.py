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
# Documentation:
#  - https://developers.google.com/api-client-library/python/
#  - https://developers.google.com/sheets/api/quickstart/python
#  - https://developers.google.com/sheets/api/guides
#  - https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/
#
# URL
#   https://docs.google.com/spreadsheets/d/spreadsheetId/edit#gid=sheetId
#                                        ([a-zA-Z0-9-_]+)
#                                                            [#&]gid=([0-9]+)
#
# A1 notation
#   Sheet1!A1:B2   refers to the first two cells in the top two rows of Sheet1.
#   Sheet1!A:A     refers to all the cells in the first column of Sheet1.
#   Sheet1!1:2     refers to the all the cells in the first two rows of Sheet1.
#   Sheet1!A5:A    refers to all the cells of the first column of Sheet 1, from row 5 onward.
#   A1:B2          refers to the first two cells in the top two rows of the first visible sheet.
#   Sheet1         refers to all the cells in Sheet1.
#
# OAuth 2.0 scope information for the Google Sheets API:
#   https://www.googleapis.com/auth/...
#   spreadsheets.readonly   Allows read-only access to the user's sheets and their properties.
#   spreadsheets            Allows read/write access to the user's sheets and their properties.
#   drive.readonly          Allows read-only access to the user's file metadata and file content.
#   drive.file              Per-file access to files created or opened by the app.
#   drive                   Full, permissive scope to access all of a user's files.
#                           Request this scope only when it is strictly necessary.
#
# OAuth Protocol Flow
#
#    Api <---> App <---> User
#
#      Instead to pass (user, password) to the App and give an insecure full access
#      We just give a token for a limited access to the API
#
#    +--------+                               +---------------+
#    |        |--(A)- Authorization Request ->|   Resource    |
#    |        |                               |     Owner     |
#    |        |<-(B)-- Authorization Grant ---|               |
#    |        |                               +---------------+
#    |        |
#    |        |                               +---------------+
#    |        |--(C)-- Authorization Grant -->| Authorization |
#    | Client |                               |     Server    |
#    |        |<-(D)----- Access Token -------|               |
#    |        |                               +---------------+
#    |        |
#    |        |                               +---------------+
#    |        |--(E)----- Access Token ------>|    Resource   |
#    |        |                               |     Server    |
#    |        |<-(F)--- Protected Resource ---|               |
#    +--------+                               +---------------+
#
####################################################################################################

####################################################################################################

####################################################################################################

import httplib2

from apiclient import discovery

from oauth2client import client, tools
from oauth2client.file import Storage

####################################################################################################

def get_credentials(application_name,
                    scope,
                    credential_path,
                    client_secret_file,
                    flags):

    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid, the OAuth2 flow is
    completed to obtain the new credentials : it will opens a browser tab and ask to connect to
    Google and authorise the access.

    client_secret_file must be downloaded from Google Developers Console

    Returns:
        Credentials, the obtained credential.

    """

    # https://developers.google.com/sheets/api/quickstart/python
    # See https://developers.google.com/api-client-library/python/guide/aaa_oauth Command-line tools

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        # creates a Flow object from a client secret JSON file,
        # storing client ID, client secret, and other OAuth 2.0 parameters.
        # http://oauth2client.readthedocs.io/en/latest/source/oauth2client.client.html#oauth2client.client.flow_from_clientsecrets
        flow = client.flow_from_clientsecrets(
            client_secret_file,
            scope,
            # redirect_uri='‘urn:ietf:wg:oauth:2.0:oob' for a non-web-based application
            # redirect_uri='http://example.com/auth_return'
        )
        flow.user_agent = application_name
        # http://oauth2client.readthedocs.io/en/latest/source/oauth2client.tools.html#oauth2client.tools.run_flow
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)

    return credentials

####################################################################################################

class Spreadsheet:

    DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

    ##############################################

    def __init__(self, credentials, spreadsheet_id):

        http = credentials.authorize(httplib2.Http())
        self._service = discovery.build(
            'sheets', 'v4',
            http=http,
            discoveryServiceUrl=self.DISCOVERY_URL)
        self._spreadsheet_id = spreadsheet_id

    ##############################################

    def _get(self):

        request = self._service.spreadsheets().get(spreadsheetId=self._spreadsheet_id)
        return request.execute()

    ##############################################

    def _values(self):

        return self._service.spreadsheets().values()

    ##############################################

    def sheet_titles(self):

        data = self._get()
        return [sheet['properties']['title'] for sheet in data['sheets']]

    ##############################################

    def get_cells(self, sheet_title, cell_range=''):

        if cell_range:
            range_name = '{}!{}'.format(sheet_title, cell_range)
        else:
            range_name = sheet_title
        request = self._values().get(
            spreadsheetId=self._spreadsheet_id,
            range=range_name,
        )
        result = request.execute()
        values = result.get('values', None) # []

        # Fixme: googleapiclient.errors.HttpError

        return values

    ##############################################

    # values = [
    #     [
    #         # Cell values ...
    #     ],
    #     # Additional rows ...
    # ]
    # body = {
    #     'values': values
    # }
    # result = service.spreadsheets().values().update(
    #     spreadsheetId=spreadsheet_id, range=range_name,
    #     valueInputOption=value_input_option, body=body,
    # ).execute()
    # print('{0} cells updated.'.format(result.get('updatedCells')))
