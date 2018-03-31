####################################################################################################
#
# Climbing Asso Portal - A Portal for Climbing Club (Association)
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from ClimbingAssoPortalTools.Math.Interval import *

####################################################################################################

class TestInterval(unittest.TestCase):

    ##############################################

    def test_constructor(self):

        # Test argument validity
        with self.assertRaises(ValueError):
            Interval(1, 0)

        # Test __getitem__ interface
        i1 = Interval(1, 10)
        for i in (i1,
                  (1, 10),
                  [1, 10],
                  ):
            self.assertEqual(i1, Interval(i))

        # Test with Interval instance
        i1 = Interval(0, 10)
        self.assertEqual(i1, Interval(i1))
        self.assertEqual(i1, IntervalInt(i1))

        # Test copy
        self.assertEqual(i1, i1.copy())

    ##############################################

    def test_length(self):

        # Test length
        i1 = Interval(1, 10)
        self.assertEqual(i1.length(), 9)
        i1 = IntervalInt(1.1, 10.1)
        self.assertEqual(i1.length(), 10)

        # Test empty
        empty = Interval(None, None)
        self.assertTrue(empty.is_empty())

    ##############################################

    def test_union(self):

        # Indenpotence
        i1 = Interval(1, 10)
        self.assertEqual(i1 | i1, i1)

        # Inside
        i1 = Interval(1, 20)
        i2 = Interval(5, 15)
        self.assertEqual(i1 | i2, i1)
        self.assertEqual(i2 | i1, i1)

        # Overlap
        i1 = Interval(1, 10)
        i2 = Interval(5, 15)
        i1_i2_union = Interval(1, 15)
        self.assertEqual(i1 | i2, i1_i2_union)
        self.assertEqual(i2 | i1, i1_i2_union)

        # Inf = Sup
        i1 = Interval(1, 10)
        i2 = Interval(10, 15)
        self.assertEqual(i1 | i2, i1_i2_union)
        self.assertEqual(i2 | i1, i1_i2_union)

        # Outside
        i1 = Interval(1, 10)
        i2 = Interval(11, 15)
        self.assertEqual(i1 | i2, i1_i2_union)
        self.assertEqual(i2 | i1, i1_i2_union)

        # |=
        i1 = Interval(0, 10)
        i2 = Interval(5, 15)
        i1 |= i2
        self.assertEqual(i1, Interval(0, 15))

    ##############################################

    def test_intersection(self):

        # Indenpotence
        i1 = Interval(1, 10)
        self.assertEqual(i1 & i1, i1)

        # Inside
        i1 = Interval(1, 20)
        i2 = Interval(5, 15)
        self.assertEqual(i1 & i2, i2)
        self.assertEqual(i2 & i1, i2)

        # Overlap
        i1 = Interval(1, 10)
        i2 = Interval(5, 15)
        i1_i2_intersection = Interval(5, 10)
        self.assertEqual(i1 & i2, i1_i2_intersection)
        self.assertEqual(i2 & i1, i1_i2_intersection)

        # Inf = Sup
        i1 = Interval(1, 10)
        i2 = Interval(10, 15)
        i1_i2_intersection = Interval(10, 10)
        self.assertEqual(i1 & i2, i1_i2_intersection)
        self.assertEqual(i2 & i1, i1_i2_intersection)

        # Outside
        i1 = Interval(1, 10)
        i2 = Interval(11, 15)
        self.assertTrue((i1 & i2).is_empty())
        self.assertTrue((i2 & i1).is_empty())

        # &=
        i1 = Interval(0, 10)
        i2 = Interval(5, 15)
        i1 &= i2
        self.assertEqual(i1, Interval(5, 10))

####################################################################################################

class TestInterval2D(unittest.TestCase):

    ##############################################

    def test_constructor(self):

        # Test __getitem__ interface
        i1 = Interval2D((1, 10), (10, 100))

        for x, y in ((Interval(1, 10), Interval(10, 100)),
                     ([1, 10], [10, 100]),
                     ):
            self.assertEqual(i1, Interval2D(x, y))

        # Test copy
        self.assertEqual(i1, i1.copy())

    ##############################################

    def test_length(self):

        i1 = Interval2D((1, 10), (10, 100))
        self.assertEqual(i1.size(), (9, 90))

        i1 = IntervalInt2D((1.1, 10.1), (10.1, 100.1))
        self.assertEqual(i1.size(), (10, 91))

    ##############################################

    def test_union(self):

        i1 = Interval2D((1, 10), (10, 100))
        i2 = Interval2D((5, 15), (50, 150))

        i1_i2_union = Interval2D((1, 15), (10, 150))
        self.assertEqual(i1 | i2, i1_i2_union)

        i1 |= i2
        self.assertEqual(i1, i1_i2_union)

    ##############################################

    def test_intersection(self):

        i1 = Interval2D((1, 10), (10, 100))
        i2 = Interval2D((5, 15), (50, 150))

        i1_i2_intersection = Interval2D((5, 10), (50, 100))
        self.assertEqual(i1 & i2, i1_i2_intersection)

        i1 &= i2
        self.assertEqual(i1, i1_i2_intersection)

####################################################################################################

class TestIntervalIntSupOpen(unittest.TestCase):

    ##############################################

    def test_intersection(self):

        # Indenpotence
        i1 = IntervalIntSupOpen(1, 10)
        self.assertEqual(i1 & i1, i1)

        # Inside
        i1 = IntervalIntSupOpen(1, 20)
        i2 = IntervalIntSupOpen(5, 15)
        self.assertEqual(i1 & i2, i2)
        self.assertEqual(i2 & i1, i2)

        # Overlap
        i1 = IntervalIntSupOpen(1, 10)
        i2 = IntervalIntSupOpen(5, 15)
        i1_i2_intersection = IntervalIntSupOpen(5, 10)
        self.assertEqual(i1 & i2, i1_i2_intersection)
        self.assertEqual(i2 & i1, i1_i2_intersection)

        # Inf = Sup
        i1 = IntervalIntSupOpen(1, 10)
        i2 = IntervalIntSupOpen(10, 15)
        i1_i2_intersection = IntervalIntSupOpen(10, 10)
        self.assertTrue((i1 & i2).is_empty())
        self.assertTrue((i2 & i1).is_empty())

        # Outside
        i1 = IntervalIntSupOpen(1, 10)
        i2 = IntervalIntSupOpen(11, 15)
        self.assertTrue((i1 & i2).is_empty())
        self.assertTrue((i2 & i1).is_empty())

    ##############################################

    def test_minus(self):

        # Overlap sup
        i1 = IntervalIntSupOpen(0, 20)
        i2 = IntervalIntSupOpen(10, 20)
        i1_minus_i2 = i1.minus(i2)
        self.assertTupleEqual(i1_minus_i2, (IntervalIntSupOpen(0, 10),))

        # Overlap inf
        i1 = IntervalIntSupOpen(0, 20)
        i2 = IntervalIntSupOpen(0, 10)
        i1_minus_i2 = i1.minus(i2)
        self.assertTupleEqual(i1_minus_i2, (IntervalIntSupOpen(10, 20),))

        # Indemp
        i1 = IntervalIntSupOpen(1, 10)
        i1_minus_i2 = i1.minus(i1)
        self.assertIsNone(i1_minus_i2)

        # Inside
        i1 = IntervalIntSupOpen(0, 20)
        i2 = IntervalIntSupOpen(5, 15)
        i1_minus_i2 = i1.minus(i2)
        self.assertTupleEqual(i1_minus_i2,
                              (IntervalIntSupOpen(0, 5),
                               IntervalIntSupOpen(15, 20)))

        # Excluded
        i1 = IntervalIntSupOpen(5, 15)
        i2 = IntervalIntSupOpen(0, 20)
        i1_minus_i2 = i1.minus(i2)
        self.assertIsNone(i1_minus_i2)

    ##############################################

    def test_exclude(self):

        # Overlap sup
        i1 = IntervalIntSupOpen(4, 16)
        i2 = IntervalIntSupOpen(8, 16)
        self.assertTupleEqual(i1.exclude(i2),
                              ((IntervalIntSupOpen(4,  8), True),
                               (IntervalIntSupOpen(8, 16), False)))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
