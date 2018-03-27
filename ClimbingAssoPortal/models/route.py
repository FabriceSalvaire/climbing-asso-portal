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
    'Route',
]

####################################################################################################

# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _

from django.db.models.fields import (
    CharField,
    DateField,
    PositiveIntegerField,
    TextField,
)

from ClimbingGrade import FrenchGrade

from ..constants import *

####################################################################################################

SPECIAL_GRADES = ['ENF']

def french_grade_validator(grade):
    if grade not in SPECIAL_GRADES:
        try:
            FrenchGrade(grade)
        except ValueError:
            raise ValidationError(_('Invalid French Grade'))

####################################################################################################

class Route(Model):

    line_number = PositiveIntegerField(
        verbose_name=_('line number'),
        null=False,
        blank=False,
    )

    grade = CharField(
        verbose_name=_('grade'),
        max_length=3,
        null=False,
        blank=False,
        validators=[french_grade_validator],
    )

    colour = PositiveIntegerField(
        verbose_name=_('colour'),
        choices=COLOUR_CHOICES,
        null=False,
        blank=False,
    )

    name = TextField(
        verbose_name=_('name'),
        null=True,
        blank=True,
    )

    comment = TextField(
        verbose_name=_('comment'),
        null=True,
        blank=True,
    )

    opener = TextField(
        verbose_name=_('opener'),
        null=True,
        blank=True,
    )

    opening_date = DateField(
        verbose_name=_('opening date'),
        null=False,
        blank=False,
    )

    ##############################################

    def __str__(self):

        template = 'Route {0.line_number} {0.grade} {0.name} {0.opening_date}'
        return template.format(self)
