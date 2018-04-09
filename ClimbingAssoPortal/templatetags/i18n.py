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
# https://github.com/MoritzS/jinja2-django-tags
#
####################################################################################################

####################################################################################################

from django.conf import settings
from django.utils import translation

from django_jinja import library

####################################################################################################

# from .myextensions import MyExtension
# library.extension(MyExtension)

####################################################################################################

@library.global_function
def get_current_language():

    """
    Usage: {{ get_current_language() }}
    """

    return translation.get_language()

####################################################################################################

@library.global_function
def get_available_languages():

    """
    Usage: {{ get_available_languages() }}
    """

    return [(key, translation.gettext(value)) for key, value in settings.LANGUAGES]

####################################################################################################

@library.global_function
def get_language_info(lang_code):

    """
    Usage: {{ get_language_info(lang_code) }}
    """

    return translation.get_language_info(lang_code)

####################################################################################################

# @library.global_function
# def get_language_info_list():

#     def get_language_info(self, language):
#         # ``language`` is either a language code string or a sequence
#         # with the language code as its first item
#         if len(language[0]) > 1:
#             return translation.get_language_info(language[0])
#         else:
#             return translation.get_language_info(str(language))

#     langs = self.languages.resolve(context)
#     [self.get_language_info(lang) for lang in langs]
