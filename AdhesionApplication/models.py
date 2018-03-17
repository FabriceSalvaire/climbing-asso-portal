# -*- mode: Python -*-

####################################################################################################

# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model, OneToOneField, CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import django.db.models as models

from django.db.models.fields import (
    BooleanField,
    CharField,
    DateField,
    PositiveIntegerField,
    TextField,
)

from account.conf import settings

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

    MIDI_GROUP = 'm'
    SOIR_GROUP = 's'
    GROUP_CHOICES = (
        (MIDI_GROUP, 'midi'),
        (SOIR_GROUP, 'soir'),
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
    ROC14 = 'roc14'
    LICENSE_CLUB_CHOICES  = (
        (ROC14, ROC14),
        ('esc15', 'Esc 15'),
        ('grimpe13', 'Grimpe 13'),
    )
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

    MALE = 'm'
    FEMALE = 'f'
    SEX_CHOICES = (
        (MALE, _('male')),
        (FEMALE, _('female')),
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
        verbose_name=_('medical certificat year'),
        null=True,
        blank=True,
        validators=[validate_year],
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

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def first_name(self):
        return self.user.first_name

    ##############################################

    def __str__(self):
        return "{0.user}".format(self)

####################################################################################################

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
