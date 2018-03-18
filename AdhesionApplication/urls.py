# -*- mode: Python -*-

####################################################################################################

from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

from rest_framework import routers

####################################################################################################
#
# Main page
#

urlpatterns = [
    path('',
         TemplateView.as_view(template_name='main.html'),
         name='home',
    ),

    path('mentions-legales',
         TemplateView.as_view(template_name='mentions-legales.html'),
         name='mentions-legales',
    ),
]

####################################################################################################
#
# Admin
#

urlpatterns += [
    path('admin/', admin.site.urls),
]

####################################################################################################
#
# Filer
#

urlpatterns += [
    path('filer/', include('filer.urls')),
]

####################################################################################################
#
# Account
#

urlpatterns += [
    path(r'account/', include('account.urls')),
]

####################################################################################################
#
# REST API
#

from .views.rest import (
    UserViewSet,
    UserProfileViewSet,
)
from .views.schema_view import schema_view

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('user_profile', UserProfileViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-docs/', schema_view),
]

####################################################################################################
#
# User Profile
#

from .views import user_profile as user_profile_views

urlpatterns += [
    path(r'user_profile/',
        login_required(user_profile_views.UserProfileListView.as_view()),
        name='user_profile.index'),

    path(r'user_profile/<int:user_profile_id>/',
        user_profile_views.details,
        name='user_profile.details',
    ),

    path(r'user_profile/create/',
        user_profile_views.create,
        name='user_profile.create',
    ),

    path(r'user_profile/<int:user_profile_id>/update/',
        user_profile_views.update,
        name='user_profile.update',
    ),

    path(r'user_profile/<int:user_profile_id>/delete/',
        user_profile_views.delete,
        name='user_profile.delete',
    ),
]
