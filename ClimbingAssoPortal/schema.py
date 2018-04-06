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

import graphene
from graphene import relay, ObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from django.contrib.auth.models import User
# from account.conf import settings
# User = settings.AUTH_USER_MODEL

from . import models as app_models

####################################################################################################

class UserType(DjangoObjectType):
    class Meta:
        model = User

class ClubType(DjangoObjectType):
    class Meta:
        model = app_models.Club

class MemberType(DjangoObjectType):
    class Meta:
        model = app_models.Member

class ClubMemberType(DjangoObjectType):
    class Meta:
        model = app_models.ClubMember

####################################################################################################

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'last_name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

class ClubNode(DjangoObjectType):
    class Meta:
        model = app_models.Club
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

class MemberNode(DjangoObjectType):
    class Meta:
        model = app_models.Member
        filter_fields = {
            'license_id': ['exact'],
            'user__last_name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

class ClubMemberNode(DjangoObjectType):
    class Meta:
        model = app_models.ClubMember
        filter_fields = {
        }
        interfaces = (relay.Node, )

####################################################################################################

class Query(ObjectType):

    all_users = graphene.List(UserType)
    all_clubs = graphene.List(ClubType)
    all_members = graphene.List(MemberType)
    all_club_members = graphene.List(ClubMemberType)

    member = graphene.Field(
        MemberType,
        last_name=graphene.String(),
    )

    ##############################################

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_clubs(self, info, **kwargs):
        return app_models.Club.objects.all()

    def resolve_all_members(self, info, **kwargs):
        print('resolve_all_categories', info, kwargs)
        return app_models.Member.objects.select_related('user').all()

    def resolve_all_club_members(self, info, **kwargs):
        return app_models.ClubMember.objects.select_related('member', 'member__user').all()

    ##############################################

    def resolve_member(self, info, **kwargs):

        last_name = kwargs.get('last_name')
        if last_name is not None:
            return app_models.Member.objects.get(user__last_name=last_name)

        return None

####################################################################################################

class QueryNode(ObjectType):

    debug = graphene.Field(DjangoDebug, name='__debug')

    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    club = relay.Node.Field(ClubNode)
    all_clubs = DjangoFilterConnectionField(ClubNode)

    member = relay.Node.Field(MemberNode)
    all_members = DjangoFilterConnectionField(MemberNode)

    club_member = relay.Node.Field(ClubMemberNode)
    all_club_members = DjangoFilterConnectionField(ClubMemberNode)

####################################################################################################

# schema = graphene.Schema(query=Query)
schema = graphene.Schema(query=QueryNode)
