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

from django.conf import settings
from django.utils import translation

from jinja2 import lexer, nodes
from jinja2.ext import Extension

####################################################################################################

class GetCurrentLanguage(Extension):

    tags = set(['get_current_language'])

    ##############################################

    def parse(self, parser):

        parser.stream.expect('name:get_current_language')
        parser.stream.expect('name:as')
        name = parser.stream.expect('name')
        lineno = name.lineno

        target = nodes.Name(name, 'store',  lineno=lineno)
        value = nodes.Const(self._get_current_language())

        return nodes.Assign(target, value, lineno=lineno)

    ##############################################

    def _get_current_language(self, *args):

        return translation.get_language()

####################################################################################################

class GetAvailableLanguages(Extension):

    tags = set(['get_available_languages'])

    ##############################################

    def parse(self, parser):

        parser.stream.expect('name:get_available_languages')
        parser.stream.expect('name:as')
        name = parser.stream.expect('name')
        lineno = name.lineno

        target = nodes.Name(name, 'store',  lineno=lineno)
        value = nodes.Const(self._get_available_languages())

        return nodes.Assign(target, value, lineno=lineno)

    ##############################################

    def _get_available_languages(self, *args):

        return [(key, translation.gettext(value)) for key, value in settings.LANGUAGES]

####################################################################################################

class DjangoI18n(GetCurrentLanguage, GetAvailableLanguages):

    """Combines all extensions to one, so you don't have to put all of them in the django settings.

    """

    _tag_class = {
        'get_current_language': GetCurrentLanguage,
        'get_available_languages': GetAvailableLanguages,
    }

    tags = set(_tag_class.keys())

    ##############################################

    def parse(self, parser):

        name = parser.stream.current.value
        cls = self._tag_class.get(name)

        if cls is None:
            parser.fail("got unexpected tag '{}'".format(name)) # pragma: no cover

        return cls.parse(self, parser)
