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
    RouteViewSet,
)
from .views.schema_view import schema_view

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('user_profile', UserProfileViewSet)
router.register('route', RouteViewSet)

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

####################################################################################################
#
# Routes
#

from .views import route as route_views

urlpatterns += [
    path(r'route/',
         login_required(route_views.RouteListView.as_view()),
         name='route.index'),

    path(r'route/<int:route_id>/',
         route_views.details,
         name='route.details',
    ),

    path(r'route/create/',
         route_views.create,
         name='route.create',
    ),

    path(r'route/<int:route_id>/update/',
         route_views.update,
         name='route.update',
    ),

    path(r'route/<int:route_id>/delete/',
         route_views.delete,
         name='route.delete',
    ),
]
