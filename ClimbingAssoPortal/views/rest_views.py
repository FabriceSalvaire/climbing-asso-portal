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
from rest_framework import viewsets, permissions
from rest_framework.response import Response

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
    serializer_class = _serializers. RouteSerializer

####################################################################################################

class ZipCodeViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = _serializers.ZipCodeSerializer

    __zip_code_database__ = None

    ##############################################

    @classmethod
    def _load_zip_code_database(cls):

        if cls.__zip_code_database__ is None:
            from FrenchZipCode import FrenchZipCodeDataBase
            cls.__zip_code_database__ = FrenchZipCodeDataBase()

    ##############################################

    def filter_queryset(self, queryset):
        return queryset

    ##############################################

    def get_queryset(self):

        self._load_zip_code_database()
        return self.__zip_code_database__.zip_codes

    ##############################################

    def retrieve(self, request, pk=None):

        # Fixme: pk, swagger show 'id'
        #    look get_object API

        self._load_zip_code_database()
        try:
            zip_code = self.__zip_code_database__[pk]
            serializer = self.get_serializer(zip_code)
            return Response(serializer.data)
        except KeyError:
            # raise Http404('Zip Code not found')
            return Response()
