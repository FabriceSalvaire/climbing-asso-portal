####################################################################################################
#
# Base Adresse Nationale
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
    'CityDataBase',
]

####################################################################################################

import json
import logging

import requests

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class CityDataBaseEntry:

    # Fixme: use slots ?

    """Class to store a French City Database Entry.

    coordinate is (longitude, latitude)

    """

    ##############################################

    @classmethod
    def from_json(cls, json_data):

        d = json_data['fields']
        coordinate = d.get('coordonnees_gps', None)
        if coordinate:
            latitude, longitude = coordinate # srid=4326
            point = (longitude, latitude)
        else:
            point = None

        return cls(
            insee_code=d['code_commune_insee'],
            name=d['nom_de_la_commune'],
            zip_code=d['code_postal'],
            libelle=d['libell_d_acheminement'],
            ligne_5=d.get('ligne_5', None),
            coordinate=point,
        )

    ##############################################

    def __init__(self, insee_code, name, zip_code, libelle, ligne_5, coordinate=None):

        self._insee_code = insee_code
        self._name = name
        self._zip_code = zip_code
        self._libelle = libelle
        self._ligne_5 = ligne_5
        self._coordinate = coordinate

    ##############################################

    def _get_coordinate(self, i):
        return self._coordinate[i] if self._coordinate else None

    ##############################################

    @property
    def insee_code(self):
        return self._insee_code

    @property
    def name(self):
        return self._name

    @property
    def zip_code(self):
        return self._zip_code

    @property
    def libelle(self):
        return self._libelle

    @property
    def ligne_5(self):
        return self._ligne_5

    @property
    def coordinate(self):
        return self._coordinate

    @property
    def latitude(self):
        return self._get_coordinate(1)

    @property
    def longitude(self):
        return self._get_coordinate(0)

####################################################################################################

class CityDataBase:

    """Class for the French City Database."""

    DOWNLOAD_URL = 'https://datanova.legroupe.laposte.fr/api/records/1.0/download'

    _logger = _module_logger.getChild('FrenchZipCodeDataBase')

    ##############################################

    def __init__(self, json_path=None):

        if json_path:
            json_data = self._load_json(json_path)
        else:
            json_data = self._download()

        self._entries = [CityDataBaseEntry.from_json(record) for record in json_data]

    ##############################################

    @classmethod
    def _load_json(cls, json_path):

        cls._logger.info('Read {}'.format(json_path))
        with open(json_path) as fh:
            # json_data = json.load(fh)
            data = fh.read().replace("'", '"') # Fix JSON ...
            json_data = json.loads(data)

        return json_data

    ##############################################

    @classmethod
    def _download(cls):

        cls._logger.info('Download data from {} ...'.format(cls.DOWNLOAD_URL))
        params = dict(dataset='laposte_hexasmal', format='json')
        response = requests.get(url=cls.DOWNLOAD_URL, params=params)
        response.raise_for_status()

        json_data = response.json()
        number_of_cities = len(json_data)
        cls._logger.info('Retrieved {:_} cities'.format(number_of_cities))
        return json_data

    ##############################################

    def __len__(self):
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)

    def __getitem__(self,_slice):
        return self._entries[_slice]
