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

__all__ = [
    'Club',
    'Member',
    'ClubMember',
]

####################################################################################################

# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, OneToOneField
# from django.db.models.signals import post_save
# from django.dispatch import receiver
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
    URLField,
)

from account.conf import settings

from ..constants import *

from .city import FrenchCity

####################################################################################################

def validate_year(value):
    if value < 1970:
        raise ValidationError(
            _('%(value)s is not a valid year'),
            params={'value': value},
        )

####################################################################################################

class AddressMixin(Model):

    """Adresse Mixin"""

    class Meta:
        abstract = True

    address = TextField(
        verbose_name=_('address'),
        blank=True,
        null=True,
    )

    city = ForeignKey(
        FrenchCity,
        verbose_name=_('city'),
        on_delete=models.DO_NOTHING,
        null=True,
    )

####################################################################################################

class Club(AddressMixin):

    """Model for club"""

    name = CharField(
        max_length=128,
        verbose_name='name',
    )

    home_page = URLField(
        null=True,
        blank=True,
        verbose_name='home page',
    )

    ##############################################

    def __str__(self):
        return self.name

####################################################################################################

class Member(AddressMixin):

    """Model for member"""

    # Fixme: implement history ?

    user = OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='member',
        verbose_name=_('user'),
        null=True,
        on_delete=models.SET_NULL, # Will lose name ...
    )

    # Fixme: How to enforce first and last name ???

    # In auth/models.py
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)

    license_club = ForeignKey(
        Club,
        verbose_name=_("club's license"),
        null=True,
        on_delete=models.SET_NULL,
    )

    license_id = PositiveIntegerField(
        verbose_name=_('license id'),
    )

    birth_date = DateField(
        verbose_name=_('birth date'),
    )

    sex = CharField(
        verbose_name=_('sex'),
        max_length=1,
        choices=SEX_CHOICES,
        default=MALE, # should be most frequent
    )

    phone_home = CharField(
        verbose_name=_('phone home'),
        max_length=16,
        null=True,
        blank=True,
    )

    phone_work = CharField(
        verbose_name=_('phone work'),
        max_length=16,
        null=True,
        blank=True,
    )

    phone_mobile = CharField(
        verbose_name=_('phone mobile'),
        max_length=16,
        null=True,
        blank=True,
    )

    avatar = FilerImageField(
        verbose_name=_('avatar'),
        related_name='member_avatar',
        null=True,
        blank=True,
    )

    # Fixme: date ???
    medical_certificate_year = PositiveIntegerField(
        verbose_name=_('medical certificate year'),
        validators=[validate_year],
    )

    medical_certificate_scan = FilerImageField(
        verbose_name=_('medical certificate scan'),
        related_name='member_medical_certificate_scan',
        null=True,
        blank=True,
    )

    medical_certificate_pdf = FilerFileField(
        verbose_name=_('medical certificate PDF'),
        related_name='member_medical_certificate_pdf',
        null=True,
        blank=True,
    )

    ##############################################

    @property
    def last_name(self):

        if self.user is not None:
            return self.user.last_name
        else:
            return None

    @property
    def first_name(self):

        if self.user is not None:
            return self.user.first_name
        else:
            return None

    # auth define get_full_name() as first last name

    @property
    def last_first_name(self):

        if self.user is not None:
            return self.user.last_name.title() + ' ' + self.user.first_name.title()
        else:
            return None

    @property
    def first_letter(self):

        if self.user is not None:
            last_name = self.user.last_name
            if last_name:
                return last_name[0]
        return ''

    ##############################################

    def __str__(self):
        return "{0.user}".format(self)

####################################################################################################

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def on_user_save(sender, instance, created, **kwargs):
#     if created:
#         Member.objects.create(user=instance)

####################################################################################################

class ClubMember(Model):

    """Model for club's member data"""

    member = OneToOneField(
        Member,
        related_name='cub_member',
        verbose_name=_('member'),
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

    social_discount = BooleanField(
        verbose_name=_('social discount'),
        default=False,
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

    def __str__(self):
        return str(self.member)

    ##############################################

    @property
    def license_id(self):

        if self.member is not None:
            return self.member.license_id
        else:
            return None

    @property
    def last_name(self):

        if self.member is not None:
            return self.member.last_name
        else:
            return None

    @property
    def first_name(self):

        if self.member is not None:
            return self.member.first_name
        else:
            return None
