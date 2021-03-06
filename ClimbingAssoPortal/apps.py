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

from django.apps import AppConfig
from django.core import serializers

# from suit.apps import DjangoSuitConfig

####################################################################################################

# print('ClimbingAssoPortal.apps')

####################################################################################################

### class SuitConfig(DjangoSuitConfig):
###
###     """Custom Suit v2 Configuration"""
###
###     list_per_page = 10

####################################################################################################

class ClimbingAssoPortalConfig(AppConfig):

    name = 'ClimbingAssoPortal' # Fixme: -> climbing_asso_portal ?
    verbose_name = 'Climbing Asso Portal'

    ##############################################

    def ready(self):

        # print('ClimbingAssoPortal.ready')

        if 'geojson_ext' not in serializers.BUILTIN_SERIALIZERS:
            serializers.BUILTIN_SERIALIZERS['geojson_ext'] = 'ClimbingAssoPortal.serializers.geojson_ext'
