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

# from account.conf import settings
# settings.AUTH_USER_MODEL
from django.contrib.auth.models import User

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.response import Response
import django_filters.rest_framework

from .. import serializers as _serializers
from .. import models as _models

####################################################################################################

class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = _serializers.UserSerializer

####################################################################################################

class MemberViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = _models.Member.objects.all()
    serializer_class = _serializers.MemberSerializer

####################################################################################################

class RouteViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = _models.Route.objects.all()
    serializer_class = _serializers.RouteSerializer

####################################################################################################

class FrenchCityViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = _models.FrenchCity.objects.all()
    serializer_class = _serializers.FrenchCitySerializer

    # to filter using http://localhost:8000/api/french_cities/?zip_code=95870
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('zip_code', 'name')
