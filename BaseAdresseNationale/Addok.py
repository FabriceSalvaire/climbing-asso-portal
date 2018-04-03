####################################################################################################
#
# Base Adresse Nationale
# Copyright (C) 2018 Fabrice Salvaire
# Copyright (C) Addok for csv
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

"""
Pour plus de clarté, les exemples de commande utilisent le package httpie.

/search/

Point d’entrée pour le géocodage.

Utiliser le paramètre q pour faire une recherche plein texte:

    http 'https://api-adresse.data.gouv.fr/search/?q=8 bd du port'

Avec limit on peut contrôler le nombre d’éléments retournés:

    http 'https://api-adresse.data.gouv.fr/search/?q=8 bd du port&limit=15'

Avec autocomplete on peut désactiver les traitements d’auto-complétion:

    http 'https://api-adresse.data.gouv.fr/search/?q=8 bd du port&autocomplete=0'

Avec lat et lon on peut donner une priorité géographique:

    http 'https://api-adresse.data.gouv.fr/search/?q=8 bd du port&lat=48.789&lon=2.789'

Les filtres type, postcode (code Postal) et citycode (code INSEE) permettent de restreindre la recherche:

    http 'https://api-adresse.data.gouv.fr/search/?q=8 bd du port&postcode=44380'

    http 'https://api-adresse.data.gouv.fr/search/?q=paris&type=street'

Le retour est un geojson FeatureCollection respectant la spec GeoCodeJSON:


    'attribution': 'BAN',
    'licence': 'ODbL 1.0',
    'query': '8 bd du port',
    'type': 'FeatureCollection',
    'version': 'draft',
    'features': [
            {
                    'properties':
                    {
                            'context': '80, Somme, Picardie',
                            'housenumber': '8',
                            'label': '8 Boulevard du Port 80000 Amiens',
                            'postcode': '80000',
                            'citycode': '80021',
                            'id': 'ADRNIVX_0000000260875032',
                            'score': 0.3351181818181818,
                            'name': '8 Boulevard du Port',
                            'city': 'Amiens',
                            'type': 'housenumber'
                    },
                    'geometry':
                    {
                            'type': 'Point',
                            'coordinates': [2.29009, 49.897446]
                    },
                    'type': 'Feature'
            },
            {
                    'properties':
                    {
                            'context': '34, Hérault, Languedoc-Roussillon',
                            'housenumber': '8',
                            'label': '8 Boulevard du Port 34140 Mèze',
                            'postcode': '34140',
                            'citycode': '34157',
                            'id': 'ADRNIVX_0000000284423783',
                            'score': 0.3287575757575757,
                            'name': '8 Boulevard du Port',
                            'city': 'Mèze',
                            'type': 'housenumber'
                    },
                    'geometry':
                    {
                            'type': 'Point',
                            'coordinates': [3.605875, 43.425232]
                    },
                    'type': 'Feature'
            }
    ]

Les attributs retournés sont :

* id : identifiant de l’adresse (non stable: actuellement identifiant IGN)
* type : type de résultat trouvé

* * housenumber : numéro "à la plaque"
* * street : position "à la voie", placé approximativement au centre de celle-ci
* * locality : lieu-dit
* * municipality : numéro "à la commune"

* score : valeur de 0 à 1 indiquant la pertinence du résultat
* housenumber : numéro avec indice de répétition éventuel (bis, ter, A, B)
* name : numéro éventuel et nom de voie ou lieu dit
* postcode : code postal
* citycode : code INSEE de la commune
* city : nom de la commune
* context : n° de département, nom de département et de région
* label : libellé complet de l’adresse

/reverse/

Point d’entrée pour le géocodage inverse.

Les paramètres lat et lon sont obligatoires:

    http 'https://api-adresse.data.gouv.fr/reverse/?lon=2.37&lat=48.357'

Le paramètre type permet forcer le type de retour:

    http 'https://api-adresse.data.gouv.fr/reverse/?lon=2.37&lat=48.357&type=street'

Même format de réponse que pour le point d’entrée /search/.

/search/csv/

Point d’entrée pour le géocodage de masse à partir d’un fichier CSV.

Le fichier csv, encodé en UTF-8 et limité actuellement à 8Mo, doit être passé via le paramètre data:

    http --timeout 600 -f POST https://api-adresse.data.gouv.fr/search/csv/ data@path/to/file.csv

Par défaut, toutes les colonnes sont concaténées pour constituer l’adresse qui sera géocodée. On
peut définir les colonnes à utiliser via de multiples paramètres columns:

    http -f POST https://api-adresse.data.gouv.fr/search/csv/ columns='voie' columns='ville' data@path/to/file.csv

Il est possible de préciser le nom d’une colonne contenant le code INSEE ou le code Postal pour limiter les recherches, exemple :

    http -f POST https://api-adresse.data.gouv.fr/search/csv/ columns='voie' columns='ville' citycode='ma_colonne_code_insee' data@path/to/file.csv

    http -f POST https://api-adresse.data.gouv.fr/search/csv/ columns='voie' columns='ville' postcode='colonne_code_postal’ data@path/to/file.csv

/reverse/csv/

Point d’entrée pour le géocodage inverse de masse à partir d’un fichier CSV.

Le fichier csv, encodé en UTF-8 et limité actuellement à 8Mo, doit être passé via le paramètre
data. Il doit contenir les colonnes latitude (ou lat) et longitude (ou lon ou lng).

    http --timeout 600 -f POST https://api-adresse.data.gouv.fr/reverse/csv/ data@path/to/file.csv

"""

####################################################################################################

import csv
import io
import logging
import time

import geojson
from geojson import Feature, FeatureCollection, Point

import requests

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Address:

    ##############################################

    def __init__(self, feature):

        self._feature = feature
        self._properties = feature.properties

    ##############################################

    @property
    def feature(self):
        return self._feature

    @property
    def coordinate(self):
        """Return (longitude, latitude)"""
        return self._feature.geometry.coordinates

    ##############################################

    @property
    def type_number(self):
        return self._properties['type']

    @property
    def is_city(self):
        return self.type == 'municipality'

    @property
    def is_house_number(self):
        return self.type == 'housenumber'

    @property
    def is_locality(self):
        return self.type == 'locality'

    @property
    def is_street(self):
        return self.type == 'street'

    ##############################################

    def __getattr__(self, key):

        """key: city, housenumber, name, postcode, score, street
        """

        return self._properties.get(key, None)

####################################################################################################

class AddokClient:

    FR_ADDOK_URL = 'http://api-adresse.data.gouv.fr'
    MAX_REQUEST_PER_SECOND = 10

    _logger = _module_logger.getChild('AddokClient')

    ##############################################

    def __init__(self, url=FR_ADDOK_URL, max_request_per_second=MAX_REQUEST_PER_SECOND):

        self._url = url

        # Request statistics
        self._timestamp = None
        self._max_request_per_second = max_request_per_second
        self._delta_min = 1 / max_request_per_second
        self._number_of_requests = 0
        self._number_of_requests_too_fast = 0
        self._delay = 0

    ##############################################

    @property
    def number_of_requests(self):
        return self._number_of_requests

    @property
    def number_of_requests_too_fast(self):
        return self._number_of_requests_too_fast

    @property
    def percent_too_fast(self):
        if self._number_of_requests:
            return self._number_of_requests_too_fast / self._number_of_requests * 100
        else:
            return 0

    @property
    def max_request_per_second(self):
        return self._max_request_per_second

    @property
    def delta_min(self):
        return self._delta_min * 1000 # ms

    @property
    def delta_mean(self):

        # ~ 110-150 ms versus 100 ms
        if self._number_of_requests:
            return self._delay / self._number_of_requests * 1000 # ms
        else:
            return None

    ##############################################

    def _get(self, service, params):

        # Sleep if requests are too fast for the server
        now = time.time()
        if self._timestamp:
            delta = now - self._timestamp
            if delta < self._delta_min:
                # self._logger.info('Addok request is too fast')
                time.sleep(self._delta_min - delta)
                self._number_of_requests_too_fast += 1
            self._delay += delta
        self._timestamp = now

        response = requests.get('{}/{}/'.format(self._url, service), params=params)
        response.raise_for_status()
        self._number_of_requests += 1

        # response.json()

        collection = geojson.loads(response.text)
        return [Address(feature) for feature in collection.features]

    ##############################################

    def search(self, query, **kwargs):

        params = dict(
            q=query,
            limit=5,
        )
        params.update(
            {key:value for key, value in kwargs.items()
             if key in ('limit', 'autocomplete', 'lat', 'lon', 'type', 'postcode', 'citycode')
            }
        )

        return self._get('search', params )

    ##############################################

    def reverse(self, longitude, latitude, type=None):

        params = dict(lon=longitude, lat=latitude)
        if type:
            params['type'] = type

        return self._get('reverse', params)

    ##############################################

    @staticmethod
    def _write_response_to_disk(filename, response, chunk_size=1024):

        with open(filename, 'wb') as fh:
            for chunk in response.iter_content(chunk_size=chunk_size):
                fh.write(chunk)

    ##############################################

    def _post(self, filename, csv_data, params={}):

        # Le fichier csv, encodé en UTF-8 et limité actuellement à 8Mo
        # Fixme: columns citycode postcode

        files = {'data': (filename, csv_data)}
        response = requests.post(self._url + '/search/csv/', files=files, params=params)
        response.raise_for_status()
        # You might want to use https://github.com/g2p/rfc6266
        content_disposition = response.headers['content-disposition']
        filename = content_disposition[len('attachment; filename="'):-1]

        return filename, response

    ##############################################

    def geocode(self, lines):

        fh = io.StringIO()
        writer = csv.writer(fh)
        writer.writerow(('address', 'postcode'))
        for address, postcode in lines:
            writer.writerow((address, postcode))
        csv_data = fh.getvalue()

        params = dict(colums='address', postcode='postcode')

        _, response = self._post('none', csv_data.encode('utf8'), params)

        fh = io.StringIO(response.text)
        reader = csv.reader(fh)
        features = []
        for i, row in enumerate(reader):
            if not i:
                continue
            (
                _address, _postcode,
                latitude, longitude,
                label, score, type_, id_,
                housenumber, name, street, postcode,
                city, context, citycode,
            ) = row
            point = Point((float(longitude), float(latitude)))
            properties = dict(
                city=city,
                citycode=citycode,
                context=context,
                housenumber=housenumber,
                id=id_,
                label=label,
                name=name,
                postcode=postcode,
                score=score,
                street=street,
                type=type_,
            )
            feature = Feature(geometry=point, properties=properties)
            features.append(feature)

        return [Address(feature) for feature in features]

    ##############################################

    def geocode_csv(self, file_path):

        # Fixme: reverse

        with open(file_path, 'rb') as fh:
            filename, response = self._post(file_path, fh.read())
            self._write_response_to_disk(filename, response)

    ##############################################

    def geocode_csv_chunked(self, file_path, filename_pattern, chunk_by):

        # Fixme: better ?

        with open(file_path, 'r') as fh:
            headers = fh.readline()
            current_lines = fh.readlines(chunk_by)
            i = 1
            while current_lines:
                current_filename = filename_pattern.format(i)
                current_csv = ''.join([headers] + current_lines)
                filename, response = self._post(current_filename, current_csv)
                self._write_response_to_disk(filename, response)
                current_lines = fh.readlines(chunk_by)
                i += 1
