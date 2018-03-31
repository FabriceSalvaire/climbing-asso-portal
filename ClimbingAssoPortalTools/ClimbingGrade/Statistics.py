####################################################################################################
#
# Climbing Grade
# Copyright (C) 2015 Fabrice Salvaire
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

from .Grade import AlpineGrade, FrenchGrade

####################################################################################################

class CounterMixin:

    ##############################################

    def __init__(self, count=0):

        self._count = count

    ##############################################

    @property
    def count(self):
        return self._count

    ##############################################

    def increment(self):
        self._count += 1

####################################################################################################

class FrenchGradeCounter(FrenchGrade, CounterMixin):

    ##############################################

    def __init__(self, grade, count=0):

        FrenchGrade.__init__(self, grade)
        CounterMixin.__init__(self, count)

    ##############################################

    def __repr__(self):
        return '{} {}'.format(FrenchGrade.__str__(self), self.count)

####################################################################################################

class AlpineGradeCounter(AlpineGrade, CounterMixin):

    ##############################################

    def __init__(self, grade, count=0):

        AlpineGrade.__init__(self, grade)
        CounterMixin.__init__(self, count)

    ##############################################

    def __repr__(self):
        return '{} {}'.format(FrenchGrade.__str__(self), self.count)

####################################################################################################

class FrenchGradeHistogram:

    __grade_class__ = FrenchGrade
    __grade_counter_class__ = FrenchGradeCounter

    ##############################################

    def __init__(self):

        self._grades = [self.__grade_counter_class__(grade)
                        for grade in self.__grade_class__.grade_iter()]
        self._grade_map = {str(grade):grade for i, grade in enumerate(self._grades)}

    ##############################################

    def __iter__(self):
        return iter(self._grades)

    ##############################################

    def increment(self, grade):
        self._grade_map[str(grade)].increment()

    ##############################################

    @property
    def domain(self):

        inf = 10
        sup = 0
        for i, grade_counter in enumerate(self._grades):
            if grade_counter.count:
                inf = min(inf, i)
                sup = max(sup, i)

        return self._grades[inf:sup +1]

####################################################################################################

class AlpineGradeHistogram(FrenchGradeHistogram):

    __grade_class__ = AlpineGrade
    __grade_counter_class__ = AlpineGradeCounter
