# -*- mode: Python -*-

####################################################################################################

from django.contrib import admin

####################################################################################################

from .models import (
    UserProfile,
)

####################################################################################################

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__last_name', 'license_id')
    list_filter = ('user__last_name', 'user__first_name')
    list_display = ('last_name', 'first_name')

####################################################################################################

admin.site.register(UserProfile, UserProfileAdmin)
