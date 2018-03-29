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

"""French Zip Code Database

* https://www.data.gouv.fr/fr/datasets/base-officielle-des-codes-postaux

* `datanova.legroupe.laposte.fr
  <https://datanova.legroupe.laposte.fr/explore/?refine.keyword=la-poste&refine.keyword=commune&sort=modified>`_

* `Base officielle des codes postaux
  < https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/?disjunctive.code_commune_insee&disjunctive.nom_de_la_commune&disjunctive.code_postal&disjunctive.libell_d_acheminement&disjunctive.ligne_5>`_

  La base officielle des codes postaux est un jeu de données qui fournit la correspondance entre les
  codes postaux et les codes INSEE des communes, de France (métropole et DOM), des TOM, ainsi que de
  MONACO.

  Ce jeu de données comprend :

  * Le nom de la commune
  * Le code INSEE de la commune
  * La ligne 5 de l'adresse postale : précision du lieu-dit associé ou du nom de la commune déléguée associée
  * Le code postal de la commune
  * Le libellé d’acheminement

* `Communes nouvelles
  <https://datanova.legroupe.laposte.fr/explore/dataset/laposte_commnouv/?disjunctive.insee&disjunctive.commune_deleguee>`_

  Ce jeu de données recense les nouvelles communes créées depuis la promulgation de la loi n°
  2015-292 du16 mars 2015 relative à l'amélioration du régime de la commune nouvelle et fournit les
  nouvelles données d’adresse correspondantes. Ces données sont fournies par le Service National de
  l’Adresse (SNA) du Groupe La Poste.

  Données fournies :

  * l'identification de la commune nouvelle siège, son code INSEE,
  * l'identification de la commune déléguée, son code INSEE (qui n’est plus actif),
  * des éléments d'écriture de l'adresse

  Les champs de données sont décrits dans le Modèle de données ci-dessous.

  Pour plus d’informations sur les communes nouvelles, consulter le site de l’Association des Maires
  de France http://www.amf.asso.fr/document/communes_nouvelles.asp.

  Les incidences sur l’adresse sont présentées dans le document public de l’AMF fourni en pièce jointe.

* `API <https://datanova.legroupe.laposte.fr/api/v1/documentation>`_

  https://datanova.legroupe.laposte.fr/api/records/1.0/download/?dataset=laposte_hexasmal&&format=json
  https://datanova.legroupe.laposte.fr/api/records/1.0/download/?dataset=laposte_laposte_commnouv&&format=json

  https://datanova.legroupe.laposte.fr/api/records/1.0/search/?dataset=laposte_hexasmal&facet=code_commune_insee&facet=nom_de_la_commune&facet=code_postal&facet=libell_d_acheminement&facet=ligne_5&refine.code_postal=95870

"""

####################################################################################################

__all__ = [
    'FrenchCity',
    # 'NewFrenchCity',
]

####################################################################################################

import hashlib

from django.contrib.gis.db.models import (
    Model,
    BigIntegerField,
    CharField,
    # DateField,
    # IntegerField,
    PointField,
)
from django.utils.translation import ugettext_lazy as _

####################################################################################################

class FrenchCity(Model):

    """
    A French address is made of these lines:

    * Ligne 1 : Identité du destinataire :
      Civilité, Titre ou Qualité + Prénom et Nom
    * Ligne 2: Complément d'identification du destinataire ou du point de remise :
      N° d'appartement ou n° de boite aux lettres, Escalier, Couloir, Étage
    * Ligne 3: Complément d'identification du point géographique :
      Entrée, Tour, Immeuble, Bâtiment, Résidence, ...
    * Ligne 4 : N° de libellée de la voie
    * Ligne 5 : Lieut-dit ou Service particulier de distribution
     ( par exemple : poste restante, boîte postale, ... )
    * Ligne 6 : Code postal et localisation de destinataire

    """

    # id = models.AutoField(primary_key=True)
    # id = CharField(
    #     primary_key=True,
    #     max_length=8,
    # )
    id = BigIntegerField(primary_key=True)

    insee_code = CharField(
        # Not unique
        max_length=5,
        verbose_name=_('Code INSEE'),
    )

    name = CharField(
        max_length=128, # Fixme: measure
        verbose_name=_('name'),
    )

    zip_code = CharField(
        max_length=5,
        verbose_name=_('ZIP Code'),
    )

    libelle = CharField(
        max_length=128, # Fixme: measure
        verbose_name=_('libéllé acheminement'),
    )

    ligne_5 = CharField(
        max_length=128, # Fixme: measure
        blank=True,
        null=True,
        verbose_name=_('ligne 5'),
    )

    coordinate = PointField(
        blank=True,
        null=True,
        verbose_name=_('GPS coordinate'),
    )

    ##############################################

    @staticmethod
    def pk_for_city(**kwargs):

        # Set the pk as a deterministic and unique 64-bit integer
        pk = kwargs['insee_code'] + kwargs['zip_code'] + kwargs['libelle'] + (kwargs['ligne_5'] or '')
        pk = pk.encode('utf-8')
        pk = hashlib.sha1(pk).hexdigest()
        pk = int(pk[:8], base=16) # 40k entriesw

        return pk

    ##############################################

    @classmethod
    def create_city(cls, **kwargs):

        pk = cls.pk_for_city(**kwargs)

        cls = cls(id=pk, **kwargs)
        # cls.save()
        return cls

    ##############################################

    def __str__(self):

        name =  '{0.zip_code} {0.libelle}'.format(self)
        if self.ligne_5:
            name += self.ligne_5
        return name

####################################################################################################

# class NewFrenchCity(Model):

#     prise_en_compte = DateField(
#         verbose_name=_('Prise en compte'),
#     )

#     insee_code_new_city = CharField(
#         max_length=5,
#         verbose_name=_('Code INSEE Commune Nouvelle'),
#     )

#     insee_code_delegate = CharField(
#         max_length=5,
#         verbose_name=_('Code INSEE Commune Déléguée (non actif)'),
#     )

#     name_delegate = CharField(
#         max_length=128, # Fixme: measure
#         verbose_name=_('Nom Commune Déléguée'),
#     )

#     insee_code_2015 = CharField(
#         max_length=5,
#         verbose_name=_('Adresse 2015 - Code INSEE'),
#     )

#     zip_code_2015 = CharField(
#         max_length=5,
#         verbose_name=_('Adresse 2015 - L6 Code Postal'),
#     )

#     ligne_5_2015 = CharField(
#         max_length=128, # Fixme: measure
#         verbose_name=_('Adresse 2015 - L5'),
#     )
