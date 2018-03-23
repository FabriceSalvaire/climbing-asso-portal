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

__all__ = [
    'AlpineGrade',
    'FrenchGrade',
]

####################################################################################################

import itertools
import re

####################################################################################################

class IncompatibleGradeError(Exception):
    pass

####################################################################################################

class FrenchGrade:

    """This class defines a French grade."""

    __grade_re__ = re.compile(r'([1-9])([a-c])?(\+|\-)?')
    __grade_plus__ = 5

    ##############################################

    @classmethod
    def old_grade_iter(cls, grade_min=1, grade_max=9):

        for major in range(grade_min, grade_max +1):
            for minor in ('-', '', '+'):
                yield cls(str(major) + minor)

    ##############################################

    @classmethod
    def grade_iter(cls, grade_min=1, grade_max=9, grade_plus=__grade_plus__):

        for major in range(grade_min, grade_max +1):
            for minor in ('a', 'b', 'c'):
                grade = str(major) + minor
                yield cls(grade)
                if major >= grade_plus:
                    yield cls(grade + '+')

    ##############################################

    def __init__(self, grade):

        grade = str(grade).lower()
        match = self.__grade_re__.match(grade)
        if match is not None:
            number, self._letter, self._sign = match.groups()
            self._number = int(number)
            if self._letter is not None:
                if self._sign == '-':
                    raise ValueError('Bad grade "{}" mixing letter and inf'.format(grade))
                elif self._sign == '+' and self._number < self.__grade_plus__:
                    raise ValueError('Bad grade "{}" with sup < {}'.format(grade, self.__grade_plus__))
        else:
            raise ValueError('Bad grade "{}"'.format(grade))

    ##############################################

    @property
    def number(self):
        return self._number

    @property
    def letter(self):
        return self._letter

    @property
    def sign(self):
        return self._sign

    ##############################################

    def __str__(self):

        grade = str(self._number)
        if self._letter is not None:
            grade += self._letter
        if self._sign is not None:
            grade += self._sign
        return grade

    ##############################################

    def __repr__(self):
        return str(self)

    ##############################################

    def __float__(self):

        value = float(self._number)
        letter = self._letter
        sign = self._sign
        if letter is not None:
            # 6a < 6a+ < 6b < 6b+ < 6c < 6c+ < 7a
            if letter == 'a':
                value += 1/4
            elif letter == 'b':
                value += 1/2
            else: # c
                value += 3/4
            if sign == "+":
                value += 1/8
        else:
            # Old system: 5 -/inf < 5 < 5 +/sup
            if sign == '-':
                value += 1/4
            elif sign is None:
                value += 1/2
            else:
                value += 3/4
        return value

    ##############################################

    def __lt__(self, other):

        # if self.is_incompatible_with(other):
        #     raise IncompatibleGradeError
        # else:
        return float(self) < float(other)

    ##############################################

    def is_old_grade(self):

        # return ((self._sign is not None and self._letter is None)
        #         or (self._sign is None and self._letter is None))
        # (A.B) + (notA.B) = B
        return self._letter is None

    ##############################################

    @property
    def standard_grade(self):

        if self.is_old_grade():
            sign = self._sign
            grade = str(self._number)
            if sign == '-':
                grade += 'a'
            elif sign is None:
                grade += 'b'
            else:
                grade += 'c'
            return self.__class__(grade)
        else:
            return self

    ##############################################

    def is_incompatible_with(self, other):

        """For exemple the grade 5c+ is incompatible with 5+."""

        # Fixme: versus is_old_grade ?
        if (self._number == other._number
            and (self._sign is not None or other._sign is not None)):
            has_letter1 = self._letter is not None
            has_letter2 = other._letter is not None
            return has_letter1 ^ has_letter2
        else:
            return False

####################################################################################################

class AlpineGrade:

    """This class defines a French alpin grade."""

    __grade_majors__ = ('EN', 'F', 'PD', 'AD', 'D', 'TD', 'ED', 'EX') # , 'ABO'
    __grade_major_descriptions__ = {
        'EN': 'Enfant',
        'F': 'Facile',
        'PD': 'Peu Difficile', # et non « Pas Difficile » !
        'AD': 'Assez Difficile',
        'D': 'Difficile',
        'TD': 'Très Difficile',
        'ED': 'Extrêmement Difficile',
        'EX': 'Exceptionnellement Difficile',
        # or
        'ABO': 'Abominablement Difficile',
    }
    __grade_major_transcription__ = {
        'EN': None,
        'F': None,
        'PD': '3',
        'AD': '4',
        'D': ('4c', '5b'),
        'TD': ('5c', '6a'),
        'ED': ('6b', '7a'),
        'EX': '7b',
    }
    __grade_minors__ = ('-', '', '+')
    __grades__ = tuple([major + minor
                        for major, minor in
                        itertools.product(__grade_majors__, __grade_minors__)])
    __grade_to_number__ = {grade:i for i, grade in enumerate(__grades__)}

    ##############################################

    @staticmethod
    def grade_iter():

        for grade in AlpineGrade.__grades__:
            yield AlpineGrade(grade)

    ##############################################

    def __init__(self, grade):

        grade = str(grade).upper()
        if grade not in self.__grades__:
            raise ValueError('Bad alpine grade "{}"'.format(grade))

        self._grade = grade
        if grade[-1] in ('-', '+'):
            self._major = grade[:-1]
            self._minor = grade[1]
        else:
            self._major = grade
            self._minor = None

    ##############################################

    def __str__(self):
        return self._grade

    ##############################################

    def __repr__(self):
        return self._grade

    ##############################################

    def __int__(self):
        return self.__grade_to_number__[self._grade]

    ##############################################

    def __float__(self):

        value = self._major
        minor = self._minor
        if minor is None:
            value += 1/2
        elif minor == '-':
            value += 1/4
        else:
            value += 3/4

        return value

    ##############################################

    def __lt__(self, other):
        return int(self) < int(other)

    ##############################################

    @property
    def major(self):
        return AlpineGrade(self._major)

    ##############################################

    @property
    def minor(self):
        return self._minor
