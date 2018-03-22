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

# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model, OneToOneField, CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import django.db.models as models

from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

from django.db.models.fields import (
    BooleanField,
    CharField,
    DateField,
    PositiveIntegerField,
    TextField,
)

from account.conf import settings

from ClimbingGrade import FrenchGrade

from .constants import *

####################################################################################################

def validate_year(value):
    if value < 1970:
        raise ValidationError(
            _('%(value)s is not a valid year'),
            params={'value': value},
        )

####################################################################################################

class UserProfile(Model):

    """This class defines a user profile."""

    # Fixme: implement history ?

    user = OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )

    # année d'inscription
    registration_year = PositiveIntegerField(
        verbose_name=_('registration year'),
        null=True,
        blank=True,
        validators=[validate_year],
    )

    group = CharField(
        verbose_name=_('group'),
        max_length=1,
        choices=GROUP_CHOICES,
        default=SOIR_GROUP,
    )

    # n° licence fsgt
    license_id = PositiveIntegerField(
        verbose_name=_('license id'),
        null=True,
        blank=True,
    )

    # club de la licence
    license_club = TextField(
        verbose_name=_("license's club"),
        choices=LICENSE_CLUB_CHOICES,
        default=ROC14,
    )

    # date de naissance
    birth_date = DateField(
        verbose_name=_('birth date'),
        null=True,
        blank=True,
    )

    sex = CharField(
        verbose_name=_('sex'),
        max_length=1,
        choices=SEX_CHOICES,
        default=MALE, # should be most frequent
    )

    adresse = TextField(
        verbose_name=_('adresse'),
        null=True,
        blank=True,
    )

    # FR-75000
    zip_code = PositiveIntegerField(
        verbose_name=_('zip code'),
        null=True,
        blank=True,
    )

    city = TextField(
        verbose_name=_('city'),
        null=True,
        blank=True,
    )

    phone_home = TextField(
        verbose_name=_('phone home'),
        null=True,
        blank=True,
    )

    phone_work = TextField(
        verbose_name=_('phone work'),
        null=True,
        blank=True,
    )

    phone_mobile = TextField(
        verbose_name=_('phone mobile'),
        null=True,
        blank=True,
    )

    medical_certificate_year = PositiveIntegerField(
        verbose_name=_('medical certificate year'),
        null=True,
        blank=True,
        validators=[validate_year],
    )

    social_discount = BooleanField(
        verbose_name=_('social discount'),
        default=False,
    )

    medical_certificate_scan = FilerImageField(
        verbose_name=_('medical certificate scan'),
        related_name="medical_certificate_scan_user_profile",
        null=True,
        blank=True,
    )

    medical_certificate_pdf = FilerFileField(
        verbose_name=_('medical certificate PDF'),
        related_name="medical_certificate_pdf_user_profile",
        null=True,
        blank=True,
    )

    # id membre
    # nom du saisisseur
    # tarif 2017/18
    # pôle1
    # pôle2
    # no chèque
    # nom titulaire du chèque
    # nom banque
    # montant total du chèque
    # commentaire

    ##############################################

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_first_name(self):
        return self.user.last_name.title() + ' ' + self.user.first_name.title()

    @property
    def first_letter(self):
        last_name = self.user.last_name
        if last_name:
            return last_name[0]
        else:
            return ''

    ##############################################

    def __str__(self):
        return "{0.user}".format(self)

####################################################################################################

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

####################################################################################################

SPECIAL_GRADES = ['ENF']

def french_grade_validator(grade):
    if grade not in SPECIAL_GRADES:
        try:
            FrenchGrade(grade)
        except ValueError:
            raise ValidationError(_('Invalid French Grade'))

####################################################################################################

class Route(Model):

    line_number = PositiveIntegerField(
        verbose_name=_('line number'),
        null=False,
        blank=False,
    )

    grade = CharField(
        verbose_name=_('grade'),
        max_length=3,
        null=False,
        blank=False,
        validators=[french_grade_validator],
    )

    colour = PositiveIntegerField(
        verbose_name=_('colour'),
        choices=COLOUR_CHOICES,
        null=False,
        blank=False,
    )

    name = TextField(
        verbose_name=_('name'),
        null=True,
        blank=True,
    )

    comment = TextField(
        verbose_name=_('comment'),
        null=True,
        blank=True,
    )

    opener = TextField(
        verbose_name=_('opener'),
        null=True,
        blank=True,
    )

    opening_date = DateField(
        verbose_name=_('opening date'),
        null=False,
        blank=False,
    )
