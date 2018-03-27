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

####################################################################################################

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError

from ClimbingAssoPortal.models import FrenchCity

import requests

####################################################################################################

class Command(BaseCommand):

    help = 'Update French cities'

    ##############################################

    def add_arguments(self, parser):

        parser.add_argument(
            '--laposte-hexasmal-json',
            help='optional path to laposte_hexasmal.json',
        )

    ##############################################

    def handle(self, *args, **options):

        json_path = options['laposte_hexasmal_json']
        if json_path:
            self.stdout.write('Read {}'.format(json_path))
            import json
            with open(json_path) as fh:
                # json_data = json.load(fh)
                data = fh.read().replace("'", '"') # Fix JSON ...
                json_data = json.loads(data)
        else:
            url = 'https://datanova.legroupe.laposte.fr/api/records/1.0/download'
            params = dict(
                dataset='laposte_hexasmal',
                format='json',
                # format='csv',
            )
            self.stdout.write('Download data from {} ...'.format(url))
            response = requests.get(url=url, params=params)
            if response.status_code == 404:
                raise CommandError('{0.text}\n\n\nServer returned HTTP 404 Not Found for {0.url}'.format(response))
            else:
                json_data = response.json()

        number_of_cities = len(json_data)
        self.stdout.write('Loaded {:_} cities'.format(number_of_cities))

        # [{
        #     'datasetid': 'laposte_hexasmal',
        #     'recordid': '71bd2056046544371683b0e2173616500f8b2607',
        #     'fields': {
        #         'nom_de_la_commune': 'MONTROZIER',
        #         'libell_d_acheminement': 'MONTROZIER',
        #         'code_postal': '12630',
        #         'coordonnees_gps': [44.3813386273, 2.71254776972],
        #         'code_commune_insee': '12157'
        #     },
        #     'geometry': {'type': 'Point', 'coordinates': [2.71254776972, 44.3813386273]
        #  },

        cities = []
        for i, record in enumerate(json_data):
            d = record['fields']
            coordinate = d.get('coordonnees_gps', None)
            if coordinate:
                latitude, longitude = coordinate
                point = Point(longitude, latitude, srid=4326)
            else:
                point = None
            city = FrenchCity(
                insee_code=d['code_commune_insee'],
                name=d['nom_de_la_commune'],
                zip_code=d['code_postal'],
                libelle_acheminement=d['libell_d_acheminement'],
                ligne_5=d.get('ligne_5', None),
                coordinate=point,
            )
            cities.append(city)
            if not i % 5_000:
                self.stdout.write('built {} % cities'.format(int(i/number_of_cities*100)))

        self.stdout.write('Delete cities ...')
        FrenchCity.objects.all().delete()
        self.stdout.write('Save cities ...')
        FrenchCity.objects.bulk_create(cities)

        self.stdout.write(self.style.SUCCESS('Success'))
