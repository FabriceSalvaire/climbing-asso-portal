# -*- mode: Python -*-

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

from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

from rest_framework import routers

from .apps import ClimbingAssoPortalConfig

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

    path('api-summary',
         login_required(TemplateView.as_view(template_name='api-summary.html')),
         name='api-summary',
    ),
]

####################################################################################################
#
# REST API
#

# Fixme: move supra ?

from .views import rest as rest_views

router = routers.DefaultRouter()
router.register('french_cities', rest_views.FrenchCityViewSet)
router.register('club', rest_views.ClubViewSet)
router.register('users', rest_views.UserViewSet)
router.register('members', rest_views.MemberViewSet)
router.register('club_members', rest_views.ClubMemberViewSet)
router.register('routes', rest_views.RouteViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

####################################################################################################
#
# REST API Doc
#

from .views.schema import schema_view

urlpatterns += [
    path('api-docs/', schema_view, name='old-swagger'),
]


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions as rest_permissions

schema_view = get_schema_view(
    openapi.Info(
        title='{} API'.format(ClimbingAssoPortalConfig.verbose_name),
        default_version='v1',
        description='Description ...',
        terms_of_service='Terms of service ...',
        contact=openapi.Contact(email='contact AT fabrice DOT salvaire .fr'),
        license=openapi.License(name='License ...'),
    ),
    # Fixme: drf_yasg.errors.SwaggerValidationError: spec validation failed
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(rest_permissions.IsAdminUser,),
)

urlpatterns += [
    re_path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]

####################################################################################################
#
# Member
#

from .views import member as member_views

urlpatterns += [
    path('member/',
         login_required(member_views.MemberListView.as_view()),
         name='member.index',
    ),

    path('member_as_csv/',
         member_views.member_as_csv,
         name='member_as_csv',
    ),

    path('member/<int:member_id>/',
         member_views.details,
         name='member.details',
    ),

    path('member/create/',
         member_views.create,
         name='member.create',
    ),

    path('member/<int:member_id>/update/',
         member_views.update,
         name='member.update',
    ),

    path('member/<int:member_id>/delete/',
         member_views.delete,
         name='member.delete',
    ),
]

####################################################################################################
#
# Routes
#

from .views import route as route_views

urlpatterns += [
    path('wall/',
         TemplateView.as_view(template_name='wall.html'),
         name='wall',
    ),

    path('route/',
         login_required(route_views.RouteListView.as_view()),
         name='route.index'),

    path('route/histogram.svg',
         route_views.route_historgam,
         name='route.histogram'),

    path('route/cumulative_histogram.svg',
         route_views.route_cumulative_histogram,
         name='route.cumulative_histogram'),

    path('route/inverse_cumulative_histogram.svg',
         route_views.route_inverse_cumulative_histogram,
         name='route.inverse_cumulative_histogram'),

    path('route/<int:route_id>/',
         route_views.details,
         name='route.details',
    ),

    path('route/create/',
         route_views.create,
         name='route.create',
    ),

    path('route/<int:route_id>/update/',
         route_views.update,
         name='route.update',
    ),

    path('route/<int:route_id>/delete/',
         route_views.delete,
         name='route.delete',
    ),
]

####################################################################################################
#
# Test Page
#

urlpatterns += [
    path('test/',
         TemplateView.as_view(template_name='test/index.html'),
         name='test.index',
    ),

    path('test/rest-ajax',
         TemplateView.as_view(template_name='test/rest-ajax.html'),
         name='test.rest-ajax',
    ),

    path('test/select2',
         TemplateView.as_view(template_name='test/select2.html'),
         name='test.select2',
    ),

    path('test/slider',
         TemplateView.as_view(template_name='test/slider.html'),
         name='test.slider',
    ),

    path('test/route-angularjs',
         TemplateView.as_view(template_name='test/index-angularjs.html'),
         name='test.route-angularjs',
    ),
]
