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
# cf. https://django-rest-swagger.readthedocs.io/en/latest/schema/
#
####################################################################################################

####################################################################################################

from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from ..apps import ClimbingAssoPortalConfig

####################################################################################################

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    # Fixme: OpenAPIRenderer json doc
    #  "detail": "Could not satisfy the request Accept header."
    title = '{} API'.format(ClimbingAssoPortalConfig.verbose_name)
    generator = schemas.SchemaGenerator(title=title)
    return response.Response(generator.get_schema(request=request))
