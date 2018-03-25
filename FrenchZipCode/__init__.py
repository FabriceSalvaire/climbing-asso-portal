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

__all__ = [
    'FrenchZipCode',
    'FrenchZipCodeDataBase',
]

####################################################################################################

import json
from pathlib import Path

from ClimbingAssoPortalTools.Singleton import SingletonMetaClass

####################################################################################################

class FrenchZipCode:

    ##############################################

    def __init__(self, zip_code, cities):

        self._zip_code = int(zip_code)
        self._cities = list(cities)

    ##############################################

    @property
    def zip_code(self):
        return self._zip_code

    @property
    def cities(self):
        return self._cities # Fixme: iter, list ?

    ##############################################

    def __int__(self):
        return self._zip_code

    ##############################################

    def __str__(self):

        if len(self._cities) == 1:
            return self._cities[0]
        else:
            return None

    ##############################################

    def __len__(self):
        return len(self._cities)

    ##############################################

    def __iter__(self):
        return iter(self._cities)

    ##############################################

    def __getitem__(self,_slice):
        return self._cities[_slice]

####################################################################################################

class FrenchZipCodeDataBase(metaclass=SingletonMetaClass):

    __json_path__ = Path(__file__).parent.joinpath('french_zip_code.json')

    ##############################################

    def __init__(self):

        self._zip_code_map = None # lazy loading

    ##############################################

    def _load(self):

        if self._zip_code_map is None:
            with open(self.__json_path__) as fh:
                data = json.load(fh)

            zip_codes = [FrenchZipCode(*args) for args in data.items()]
            self._zip_codes = zip_codes

            self._zip_code_map = {int(zip_code):zip_code for zip_code in zip_codes}

            self._city_map = {}
            for zip_code in zip_codes:
                for city in zip_code:
                    if city not in self._city_map:
                        self._city_map[city] = [zip_code]
                    else:
                        self._city_map[city].append(zip_code)

    ##############################################

    @property
    def zip_codes(self):
        self._load()
        return self._zip_codes

    @property
    def _lazy_zip_codes(self):
        self._load()
        return self._zip_codes

    @property
    def _lazy_zip_code_map(self):
        self._load()
        return self._zip_code_map

    @property
    def _lazy_city_map(self):
        self._load()
        return self._city_map

    ##############################################

    def __len__(self):
        return len(self._lazy_zip_codes)

    ##############################################

    def __iter__(self):
        return iter(self._lazy_zip_codes)

    ##############################################

    def __getitem__(self, zip_code):
        return self._lazy_zip_code_map[int(zip_code)]

    ##############################################

    def zip_code_for(self, city):

        city = str(city).upper()
        zip_codes = [int(zip_code) for zip_code in self._lazy_city_map[city]]
        zip_codes.sort()
        return list(zip_codes)

    ##############################################

    def complete_city(self, prefix):

        # Fixme: speedup using prefix cache
        # Fixme: sort
        prefix = prefix.upper()
        for city in self._lazy_city_map.keys():
            if city.startswith(prefix):
                yield city

    ##############################################

    @staticmethod
    def departement_number(zip_code):

        zip_code = int(zip_code)
        if zip_code >= 97000:
            return zip_code // 100
        else:
            return zip_code // 1000

    ##############################################

    @classmethod
    def departement(cls, zip_code):

        return cls.__departements__[cls.departement_number(zip_code)]

####################################################################################################

FrenchZipCode.__departements__ = {
    # En France métropolitaine
    1: "Ain",
    2: "Aisne",
    3: "Allier",
    4: "Alpes-de-Haute-Provence",
    5: "Hautes-Alpes",
    6: "Alpes-Maritimes",
    7: "Ardèche",
    8: "Ardennes",
    9: "Ariège",
    10: "Aube",
    11: "Aude",
    12: "Aveyron",
    13: "Bouches-du-Rhône",
    14: "Calvados",
    15: "Cantal",
    16: "Charente",
    17: "Charente-Maritime",
    18: "Cher",
    19: "Corrèze",
    20: "Corse",
    '2A': "Corse-du-Sud",
    '2B': "Haute-Corse",
    21: "Côte-d'Or",
    22: "Côtes-d'Armor",
    23: "Creuse",
    24: "Dordogne",
    25: "Doubs",
    26: "Drôme",
    27: "Eure",
    28: "Eure-et-Loir",
    29: "Finistère",
    30: "Gard",
    31: "Haute-Garonne",
    32: "Gers",
    33: "Gironde",
    34: "Hérault",
    35: "Ille-et-Vilaine",
    36: "Indre",
    37: "Indre-et-Loire",
    38: "Isère",
    39: "Jura",
    40: "Landes",
    41: "Loir-et-Cher",
    42: "Loire",
    43: "Haute-Loire",
    44: "Loire-Atlantique",
    45: "Loiret",
    46: "Lot",
    47: "Lot-et-Garonne",
    48: "Lozère",
    49: "Maine-et-Loire",
    50: "Manche",
    51: "Marne",
    52: "Haute-Marne",
    53: "Mayenne",
    54: "Meurthe-et-Moselle",
    55: "Meuse",
    56: "Morbihan",
    57: "Moselle",
    58: "Nièvre",
    59: "Nord",
    60: "Oise",
    61: "Orne",
    62: "Pas-de-Calais",
    63: "Puy-de-Dôme",
    64: "Pyrénées-Atlantiques",
    65: "Hautes-Pyrénées",
    66: "Pyrénées-Orientales",
    67: "Bas-Rhin",
    68: "Haut-Rhin",
    69: "Rhône",
    '69D': "Rhône",
    '69M': "Métropole de Lyon",
    70: "Haute-Saône",
    71: "Saône-et-Loire",
    72: "Sarthe",
    73: "Savoie",
    74: "Haute-Savoie",
    75: "Paris",
    76: "Seine-Maritime",
    77: "Seine-et-Marne",
    78: "Yvelines",
    79: "Deux-Sèvres",
    80: "Somme",
    81: "Tarn",
    82: "Tarn-et-Garonne",
    83: "Var",
    84: "Vaucluse",
    85: "Vendée",
    86: "Vienne",
    87: "Haute-Vienne",
    88: "Vosges",
    89: "Yonne",
    90: "Territoire de Belfort",
    91: "Essonne",
    92: "Hauts-de-Seine",
    93: "Seine-Saint-Denis",
    94: "Val-de-Marne",
    95: "Val-d'Oise",

    # Départements d’outre-mer
    971: "Guadeloupe",
    972: "Martinique",
    973: "Guyane",
    974: "La Réunion",
    976: "Mayotte",
}
