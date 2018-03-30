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
    'field_to_verbose_name',
]

####################################################################################################

from django.apps import apps

# from account.conf import settings
# settings.AUTH_USER_MODEL
from django.contrib.auth.models import User

from ..apps import ClimbingAssoPortalConfig

climbing_asso_portal_config = apps.get_app_config(ClimbingAssoPortalConfig.name)

####################################################################################################

def field_to_verbose_name(field):

    # https://docs.djangoproject.com/en/2.0/ref/applications/#django.apps.AppConfig.get_model
    # https://docs.djangoproject.com/en/2.0/ref/models/meta/#retrieving-a-single-field-instance-of-a-model-by-name

    model_name, field_name = field.split('.')
    if model_name == 'User':
        model = User
    else:
        model = climbing_asso_portal_config.get_model(model_name)

    return model._meta.get_field(field_name).verbose_name
