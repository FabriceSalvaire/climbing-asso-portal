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

    path('about',
         TemplateView.as_view(template_name='about.html'),
         name='about',
    ),

    path('mentions-legales',
         TemplateView.as_view(template_name='mentions-legales.html'),
         name='mentions-legales',
    ),
]

####################################################################################################
#
# REST API
#

# Fixme: move supra ?

from .views import rest as rest_views

router = routers.DefaultRouter()
# Fixme: check base_name
router.register('french_cities', rest_views.FrenchCityViewSet) # , base_name='french_cities'
router.register('clubs', rest_views.ClubViewSet) # , base_name='club'
router.register('users', rest_views.UserViewSet) # , base_name='user'
router.register('members', rest_views.MemberViewSet, base_name='member')
router.register('member_auto_complete', rest_views.MemberAutoCompleteViewSet, base_name='member_auto_complete')
router.register('club_members', rest_views.ClubMemberViewSet) # , base_name='club_member'
router.register('routes', rest_views.RouteViewSet) # , base_name='route'

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

from graphene_django.views import GraphQLView

urlpatterns += [
    path('graphql', GraphQLView.as_view(graphiql=True), name='graphql'), # , schema=schema
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

    path('member/members.csv',
         member_views.member_as_csv,
         name='member.member_list_csv',
    ),

    path('member/data/',
         login_required(TemplateView.as_view(template_name='member/data.html')),
         name='member.data',
    ),

    path('member/age_histogram.svg',
         member_views.age_histogram_svg,
         name='member.age_histogram_svg'),

    path('member/age_histogram_error.svg',
         member_views.age_histogram_error_svg,
         name='member.age_histogram_error_svg'),

    path('member/age_histogram.csv',
         member_views.age_histogram_csv,
         name='member.age_histogram_csv'),

    path('member/statistics/',
         login_required(TemplateView.as_view(template_name='member/statistics.html')),
         name='member.statistics',
    ),

    path('member/member_city.json',
         member_views.member_city_geojson,
         name='member.city_geojson'),

    path('member/map/',
         login_required(TemplateView.as_view(template_name='member/map.html')),
         name='member.map',
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
    path('wall/route/',
         TemplateView.as_view(template_name='wall/route/index.html'),
         name='wall.route.index',
    ),

    path('wall/route/index-static/',
         login_required(route_views.RouteListView.as_view()),
         name='wall.route.index-static'),

    path('wall/statistics',
         TemplateView.as_view(template_name='wall/statistics.html'),
         name='wall.statistics',
    ),

    path('wall/route/histogram.svg',
         route_views.route_historgam_svg,
         name='wall.route.histogram_svg'),

    path('wall/route/cumulative_histogram.svg',
         route_views.route_cumulative_histogram_svg,
         name='wall.route.cumulative_histogram_svg'),

    path('wall/route/<int:route_id>/',
         route_views.details,
         name='wall.route.details',
    ),

    path('wall/route/create/',
         route_views.create,
         name='wall.route.create',
    ),

    path('wall/route/<int:route_id>/update/',
         route_views.update,
         name='wall.route.update',
    ),

    path('wall/route/<int:route_id>/delete/',
         route_views.delete,
         name='wall.route.delete',
    ),
]

####################################################################################################
#
# Development / Test Page
#

from .views import test as test_views

urlpatterns += [
    path('devel/api-summary',
         login_required(TemplateView.as_view(template_name='devel/api-summary.html')),
         name='devel.api-summary',
    ),

    path('devel/test/',
         login_required(TemplateView.as_view(template_name='devel/test/index.html')),
         name='devel.test.index',
    ),

    # /!\ Not in Production /!\

    path('devel/test/rest-ajax',
         TemplateView.as_view(template_name='devel/test/rest-ajax.html'),
         name='devel.test.rest-ajax',
    ),

    path('devel/test/select2',
         TemplateView.as_view(template_name='devel/test/select2.html'),
         name='devel.test.select2',
    ),

    path('devel/test/django_selet2',
         test_views.test_django_selet2,
         # test_views.TemplateFormView.as_view(),
         name='devel.test.django_select2',
    ),

    path('devel/test/slider',
         TemplateView.as_view(template_name='devel/test/slider.html'),
         name='devel.test.slider',
    ),

    path('devel/test/route-angularjs',
         TemplateView.as_view(template_name='devel/test/index-angularjs.html'),
         name='devel.test.route-angularjs',
    ),

    path('devel/test/translation',
         TemplateView.as_view(template_name='devel/test/translation.html'),
         name='devel.test.translation',
    ),

    path('devel/test/context',
         TemplateView.as_view(template_name='devel/test/context.html'),
         name='devel.test.context',
    ),
]
