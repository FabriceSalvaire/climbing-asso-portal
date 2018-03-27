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
# Django REST Framework Serializers
#
####################################################################################################

####################################################################################################

# from account.conf import settings
# settings.AUTH_USER_MODEL
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from . import models

####################################################################################################

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'email')

####################################################################################################

class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Member
        # fields = '__all__'
        exclude = (
            # 'user',
            'medical_certificate_scan',
            'medical_certificate_pdf',
        )

####################################################################################################

class RouteSerializer(serializers.HyperlinkedModelSerializer):

    # Fixme: swagger don't show descriptions for colour

    class Meta:
        model = models.Route
        fields = '__all__'

####################################################################################################

class FrenchCitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.FrenchCity
        fields = '__all__'
