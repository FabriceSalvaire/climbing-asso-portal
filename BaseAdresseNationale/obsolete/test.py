####################################################################################################
#
# French Zip Code
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

import unittest

####################################################################################################

from FrenchZipCode import *

####################################################################################################

class TestFrenchZipCode(unittest.TestCase):

    ##############################################

    def test(self):

        french_zip_code_db = FrenchZipCodeDataBase()

        for zip_code, city in (
                (95870, 'BEZONS'),
                (75001, 'PARIS'),
                (75020, 'PARIS'),
                ):
            zip_code_obj = french_zip_code_db[zip_code]
            self.assertEqual(int(zip_code_obj), zip_code)
            self.assertEqual(str(zip_code_obj), city)
            self.assertEqual(zip_code_obj[0], city)
            self.assertTrue(zip_code in french_zip_code_db.zip_code_for(city))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
