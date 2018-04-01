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

__all__= [
    'FEMALE', 'MALE',
    'SEX_CHOICES',
    'MIDI_GROUP', 'SOIR_GROUP',
    'GROUP_CHOICES',
    'COLOUR_CHOICES',
]

####################################################################################################

from django.utils.translation import ugettext_lazy as _

####################################################################################################

MALE = 'm'
FEMALE = 'f'
SEX_CHOICES = (
    (MALE, _('male')),
    (FEMALE, _('female')),
)

####################################################################################################

MIDI_GROUP = 'm'
SOIR_GROUP = 's'
GROUP_CHOICES = (
    (MIDI_GROUP, _('midi')),
    (SOIR_GROUP, _('soir')),
)

####################################################################################################

COLOURS = (
    # Keep order to don't break db
    _('black'),
    _('white'),
    #
    _('blue'),
    _('green'),
    _('red'),
    # cyan
    _('violet'), # magenta fuchsia
    _('yellow'),
    #
    _('orange'),
    _('pink'),
    _('salmon'),
    #
    _('red & white'),
)

COLOUR_CHOICES = [(i, colour) for i, colour in enumerate(COLOURS)]

####################################################################################################

ONE_HOUR = 60 * 60 # s
