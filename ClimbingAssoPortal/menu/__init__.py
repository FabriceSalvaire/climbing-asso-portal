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

__all__ = [
    'left_sidebar_menu',
]

####################################################################################################

from django.utils.translation import ugettext as _

from .Menu import Menu

####################################################################################################

left_sidebar_menu = Menu(name='left_sidebar')

Menu(
    title=_('Dashboard'),
    icon='fa-home',
    url='home',
    match='home',
    parent=left_sidebar_menu,
)

member_menu = Menu(
    title=_('Member'),
    icon='fa-users',
    parent=left_sidebar_menu,
    match='member.',
    childs=[
        Menu(
            title=_('Member List'),
            icon='fa-list',
            url='member.index',
        ),
        Menu(
            title=_('Member Map'),
            icon='fa-map',
            url='member.map',
        ),
        Menu(
            title=_('Member Statistics'),
            icon='fa-chart-bar',
            url='member.statistics',
        ),
    ],
)

wall_menu = Menu(
    title=_('Wall'),
    icon='fa-tree',
    parent=left_sidebar_menu,
    match='route.',
    childs=[
        Menu(
            title=_('Routes'),
            icon='fa-list',
            url='route.index',
        ),
    ],
)

wall_menu = Menu(
    title=_('Development'),
    icon='fa-cog',
    parent=left_sidebar_menu,
    match='devel.',
    childs=[
        Menu(
            title=_('Test Pages'),
            icon='fas.fa-vial',
            url='devel.test.index',
        ),
    ],
)
