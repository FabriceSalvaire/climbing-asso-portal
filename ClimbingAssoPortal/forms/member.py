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
    'UserStandardForm',
    'MemberForm',
    'ClubMemberForm',
]

####################################################################################################

from django.forms import ModelForm
# from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
# from account.conf import settings
# User = settings.AUTH_USER_MODEL

from .. import models as app_models

####################################################################################################

class UserStandardForm(ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name')

####################################################################################################

class MemberForm(ModelForm):
    class Meta:
        model = app_models.Member
        # fields = '__all__'
        exclude = ['user', 'city'] # Fixme

####################################################################################################

class ClubMemberForm(ModelForm):
    class Meta:
        model = app_models.ClubMember
        # fields = '__all__'
        exclude = ['member']
