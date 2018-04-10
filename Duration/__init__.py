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

"""Module to implement duration in second.

Example of usage::

    dt = 10@u_s
    dt = 2@u_hour
    dt = 10@u_day

    dt * 2
    2 * dt

    int(dt)
    float(dt)
    str(dt)

"""

####################################################################################################

__all__ = [
    'Duration',
    'u_s',
    'u_hour',
    'u_day',
]

####################################################################################################

class Duration:

    ##############################################

    def __init__(self, value):

        self._value = value

    ##############################################

    def __int__(self):

        return int(self._value)

    ##############################################

    def __float__(self):

        return float(self._value)

    ##############################################

    def __str__(self):

        return str(self._value)

    ##############################################

    def __mul__(self, other):

        return Duration(self._value * float(other))

    ##############################################

    def __mul__(self, other):

        return Duration(float(self) * float(other))

    ##############################################

    def __rmul__(self, other):
        return self.__mul__(other)

    ##############################################

    def __rmatmul__(self, other):
        return self.__mul__(other)

####################################################################################################

u_s = Duration(1)
u_min = Duration(60)
u_hour = u_min * 60
u_day = u_hour * 24
