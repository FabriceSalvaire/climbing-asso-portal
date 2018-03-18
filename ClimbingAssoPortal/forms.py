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

from django.forms import ModelForm, Form
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile

####################################################################################################

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        fields = [
            'registration_year',
            'group',
            'license_id',
            'license_club',
            'birth_date',
            'sex',
            'adresse',
            'zip_code',
            'city',
            'phone_home',
            'phone_work',
            'phone_mobile',
            'medical_certificate_year',
            'social_discount',
        ]

####################################################################################################

# class UserProfileForm(forms.Form):

    # email = forms.EmailField(
    #     label=_("Email"),
    #     widget=forms.TextInput(),
    #     required=True,
    # )

    # registration_year = forms.PositiveIntegerField(
    # )

    # group = CharField(
    # license_id = PositiveIntegerField(
    # license_club = TextField(
    # birth_date = DateField(
    # sex = CharField(
    # adresse = TextField(
    # zip_code = PositiveIntegerField(
    # city = TextField(
    # phone_home = TextField(
    # phone_work = TextField(
    # phone_mobile = TextField(
    # medical_certificate_year = PositiveIntegerField(
    # social_discount = BooleanField(
