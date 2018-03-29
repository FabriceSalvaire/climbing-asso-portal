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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from reversion.admin import VersionAdmin

####################################################################################################

from . import models

####################################################################################################

# admin.site.unregister(SomeModel)

# @admin.register(SomeModel)
# class YourModelAdmin(VersionAdmin, SomeModelAdmin):
#     pass

####################################################################################################

@admin.register(models.FrenchCity)
class FrenchCityAdmin(admin.ModelAdmin):
    # Fixme: slow ...
    search_fields = ('zip_code', 'name')
    list_display = ('name', 'zip_code')

####################################################################################################

@admin.register(models.Club)
# class MemberAdmin(admin.ModelAdmin):
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

@admin.register(models.Member)
# class MemberAdmin(admin.ModelAdmin):
class MemberAdmin(VersionAdmin):
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

@admin.register(models.ClubMember)
# class MemberAdmin(admin.ModelAdmin):
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

####################################################################################################

@admin.register(models.Route)
class RouteAdmin(admin.ModelAdmin):
# class RouteAdmin(VersionAdmin):
    # search_fields = []
    # list_filter = []
    list_display = ['line_number', 'grade', 'name']

####################################################################################################

# admin.site.register(Member, MemberAdmin)
