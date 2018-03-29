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

# from django.contrib import admin
# from django.db import models
from django.contrib.gis import admin
from django.contrib.gis.db import models as db_models

from django import forms
from django.utils.translation import ugettext_lazy as _

from reversion.admin import VersionAdmin

from .. import models

####################################################################################################

class FormFieldOverridesMixin:

    formfield_overrides = {
        db_models.CharField: {'widget': forms.TextInput()},
        db_models.TextField: {'widget': forms.Textarea(attrs={'rows':4, 'style':'width: 40%'})},
    }

####################################################################################################

@admin.register(models.Club)
class MemberAdmin(VersionAdmin):

    search_fields = ['name']
    list_display = ['name']

    # endoint is http://localhost:8000/admin/ClimbingAssoPortal/frenchcity/autocomplete/?term=bez
    autocomplete_fields = ['city']

    fieldsets = [
        [_('Identity'), {
            'fields': [
                'name',
            ]
        }],
        [_('Address'), {
            'fields': [
                'address',
                'city',
            ]
        }],
    ]

####################################################################################################

@admin.register(models.Member)
class MemberAdmin(FormFieldOverridesMixin, VersionAdmin):

    search_fields = ['user__last_name', 'license_id']
    list_display = ['last_name', 'first_name', 'license_id']

    autocomplete_fields = ['city']

    fieldsets = [
        [_('User'), {
            'fields': [
                'user',
                'avatar',
                'birth_date',
                'sex',
            ]
        }],
        [_('License'), {
            'fields': [
                'license_id',
                'license_club',
            ]
        }],
        [_('Address'), {
            'fields': [
                'address',
                'city',
            ]
        }],
        [_('Contact'), {
            'fields': [
                'phone_mobile',
                'phone_home',
                'phone_work',
            ]
        }],
        [_('Medical Certificate'), {
            'fields': [
                'medical_certificate_year',
                'medical_certificate_scan',
                'medical_certificate_pdf',
            ]
        }],
    ]

####################################################################################################

@admin.register(models.ClubMember)
class MemberAdmin(VersionAdmin):

    search_fields = ['member__user__last_name', 'member__user__first_name', 'member__license_id']
    list_display = ['last_name', 'first_name', 'license_id']

    fieldsets = [
        [_('Member'), {
            'fields': [
                'member',
            ]
        }],
        [_('Adhesion'), {
            'fields': [
                'group',
                'social_discount',
                'registration_year',
            ]
        }],
    ]
