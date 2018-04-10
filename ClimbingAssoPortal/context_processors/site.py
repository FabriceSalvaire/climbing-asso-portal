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

from django.contrib.sites.models import Site

# from .conf import settings
from django.conf import settings

####################################################################################################

def site(request):

    context = {
        # Used by account
        # 'THEME_ADMIN_URL': settings.THEME_ADMIN_URL,
        'THEME_CONTACT_EMAIL': settings.THEME_CONTACT_EMAIL,
    }

    if Site._meta.installed:
        site = Site.objects.get_current(request)
        context.update({
            'SITE_NAME': site.name,
            'SITE_DOMAIN': site.domain
        })

    return context
