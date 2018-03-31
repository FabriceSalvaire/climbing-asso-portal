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
from rest_framework import viewsets, permissions, generics, mixins, filters
from rest_framework.response import Response
import django_filters.rest_framework

from .. import serializers as _serializers
from .. import models as app_models

####################################################################################################

class FrenchCityViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = app_models.FrenchCity.objects.all()
    serializer_class = _serializers.FrenchCitySerializer

    # to filter using http://localhost:8000/api/french_cities/?zip_code=95870
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('zip_code', 'name')

####################################################################################################

class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = _serializers.UserSerializer

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('username', 'last_name')

####################################################################################################

class ClubViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = app_models.Club.objects.all()
    serializer_class = _serializers.ClubSerializer

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('name',)

####################################################################################################

class MemberAutoCompleteViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = app_models.Member.objects.order_by('user__last_name' , 'user__first_name')
    serializer_class = _serializers.MemberAutoCompleteSerializer

    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_fields = ('license_id', 'user__last_name')

    filter_backends = (filters.SearchFilter,)
    search_fields = ('=license_id', '^user__last_name')

####################################################################################################

class MemberViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = app_models.Member.objects.all()
    serializer_class = _serializers.MemberSerializer

    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('license_id', 'user__last_name')

    filter_backends = (filters.SearchFilter,)
    search_fields = ('=license_id', '^user__last_name')

####################################################################################################

class ClubMemberViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = app_models.ClubMember.objects.all()
    serializer_class = _serializers.ClubMemberSerializer

####################################################################################################

class RouteViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = app_models.Route.objects.all()
    serializer_class = _serializers.RouteSerializer
