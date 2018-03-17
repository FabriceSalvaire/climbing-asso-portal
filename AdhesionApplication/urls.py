# -*- mode: Python -*-

####################################################################################################

from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

####################################################################################################
#
# Main page
#

urlpatterns = [
    path(r'',
         TemplateView.as_view(template_name='main.html'),
         name='home',
    ),
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
# User Profile
#

from .views import user_profile as user_profile_views

urlpatterns += [
    # url(r'user_profile/',
    #     login_required(user_profile_views.UserProfileListView.as_view()),
    #     name='user_profile.index'),

    path(r'user_profile/<int:person_id>/',
        user_profile_views.details,
        name='user_profile.update',
    ),

    path(r'user_profile/<int:person_id>/create/',
        user_profile_views.create,
        name='user_profile.create',
    ),

    path(r'user_profile/<int:person_id>/update/',
        user_profile_views.update,
        name='user_profile.update',
    ),

    path(r'user_profile/<int:person_id>/delete/',
        user_profile_views.delete,
        name='user_profile.delete',
    ),
]
