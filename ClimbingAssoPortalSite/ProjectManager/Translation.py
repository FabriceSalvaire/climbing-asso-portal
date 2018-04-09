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
# See also ./manage.py makemessages
#   but --exclude is tricky
#
# extract       -> translation catalog template : /locale/message.pot
# init / update -> translation catalog            /locale/fr/LC_MESSAGES/message.po
# compile       ->                                                       message.mo
#
#  pot (Portable Object Template) : all the translation strings left empty
#  mo  (Message Object)
#
# https://github.com/python-babel/django-babel
#
#
####################################################################################################

__all__ = [
    'MakeMessage',
]

####################################################################################################

from pathlib import Path
import json
import os
import subprocess

from babel.messages import pofile

import colors # ansicolors

from . import LogPrinting

####################################################################################################

class MakeMessage:

    ##############################################

    def __init__(self, application, domain='django'):

        self._application = application
        self._domain = domain

        self._source_path = Path(__file__).parents[2].resolve()
        self._locale_dir = self._source_path.joinpath(self._application, 'locale')
        self._babel_cfg_path = self._locale_dir.joinpath('babel.cfg')
        self._pot_path = self._locale_dir.joinpath(self._domain + '.pot')

    ##############################################

    def _print_banner(self, title, width=50):

        print(
            colors.green(
                LogPrinting.format_message_header(
                    title,
                    width=width,
                    centered=True,
                    margin=True,
                    border=True,
                    bottom_rule=True,
                    newline=False,
                )
            )
        )

    ##############################################

    def extract(self):

        self._print_banner('Extract Messages ...')

        # Extract localizable messages from a collection of source files
        subprocess.call(('pybabel', 'extract',
                         '-F', self._babel_cfg_path,   # path to the extraction mapping file
                         '-k', 'lazy_gettext',   # keywords to look for in addition to the defaults
                         '-o', self._pot_path, # path to the output POT file
                         self._source_path))

    ##############################################

    def po_file(self, language):

        return self._locale_dir.joinpath(language, 'LC_MESSAGES', self._domain + '.po')

    ##############################################

    def init(self):

        self._print_banner('Init languages ...')

        for language in ('en', 'fr'):
            if not self.po_file(language).exists():
                # Create a new translations catalog based on a PO template file
                subprocess.call((
                    'pybabel', 'init',
                    '-D', self._domain,           # domain of PO file (default 'messages')
                    '-i', self._pot_path, # name of the input file
                    '-d', self._locale_dir,       # path to output directory
                    '-l', language,               # locale for the new localized catalog
                ))

    ##############################################

    def update(self):

        self._print_banner('Update messages ...')

        # Update an existing new translations catalog based on a PO template file
        subprocess.call((
            'pybabel', 'update',
            '-D', self._domain,
            '-i', self._pot_path,
            '-d', self._locale_dir,
        ))

    ##############################################

    def compile(self):

        self._print_banner('Compile messages ...')

        subprocess.call((
            'pybabel', 'compile',
            '-D', self._domain,
            '-d', self._locale_dir,
        ))

    ##############################################

    def edit_po(self, language, program='poedit'):

        subprocess.call((
            'poedit',
            self.po_file(language),
        ))

    ##############################################

    def check(self, language):

        with open(self.po_file(language)) as fh:
            catalog = pofile.read_po(fh)

            for error in catalog.check():
                print(colors.red(error))

            number_of_messages = len(catalog)
            number_of_messages_translated = 0
            for message in catalog:
                if message.context and not message.string:
                    number_of_messages_translated += 1
            print('Translated for {} : {}/{}'.format(language, number_of_messages_translated, number_of_messages))

    ##############################################

    def _merge_json(self, json_path, catalog):

        with open(json_path) as fh:
            json_data = json.load(fh)
        for message in json_data:
            catalog.add(id=message['defaultMessage'], context=message['id'], locations=[(str(json_path), 0)])

    ##############################################

    def merge_js_messages(self, json_path_root):

        with open(self._pot_path) as fh:
            catalog = pofile.read_po(fh)

        for root, _, files in os.walk(Path(json_path_root).resolve()):
            root = Path(root)
            for filename in files:
                if filename.endswith('json'):
                    absolute_filename = root.joinpath(filename)
                    self._merge_json(absolute_filename, catalog)

        with open(self._pot_path, 'wb') as fh:
            pofile.write_po(fh, catalog)

    ##############################################

    def _iter_on_language_directories(self):

        for language in self._locale_dir.iterdir():
            if language.is_dir():
                yield language

    ##############################################

    def _extract_js_for_language(self, po_file):

        with open(po_file) as fh:
            catalog = pofile.read_po(fh)

        messages = {}
        for message in catalog:
            if message.string:
                for location in message.locations:
                    if location[0].endswith('.json'):
                        messages[message.id] = message.string
                        break
        return messages

    ##############################################

    def extract_js_messages(self):

        json_data = {}
        for language_directory in self._iter_on_language_directories():
            language = language_directory.name
            po_file = self.po_file(language)
            if po_file.exists():
                messages = self._extract_js_for_language(po_file)
                json_data[language] = messages

        json_path = self._locale_dir.joinpath(self._domain + '.json')
        with open(json_path, 'w') as fh:
            json.dump(json_data, fh)
