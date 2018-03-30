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

"""ClimbingAssoPortalSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

####################################################################################################

# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.urls import include, path

####################################################################################################

urlpatterns = [
    # Common part
    path('admin/', admin.site.urls),
    # Admin install this autocomplete feature where term are searched in search_fields
    # /admin/APPLICATION/MODEL/autocomplete/?term=XYZ

    path('filer/', include('filer.urls')),
    path('account/', include('account.urls')),
    path('select2/', include('django_select2.urls')),

    path('', include('ClimbingAssoPortal.urls')),
]

####################################################################################################

# For devel only !
if settings.MEDIA_ROOT and settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=str(settings.MEDIA_ROOT))
    urlpatterns += static(settings.PRIVATE_MEDIA_URL, document_root=str(settings.PRIVATE_MEDIA_ROOT))
