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

import csv

from django.contrib import messages
from django.db.models import Q
from django.forms import ModelForm, Form, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, FormView

# from django.contrib.auth.decorators import login_required
from account.decorators import login_required

import reversion
from reversion.views import RevisionMixin

from ..forms import MemberForm
from ..models import Member, ClubMember
from ..models.Tools import field_to_verbose_name

####################################################################################################

class MemberFormView(RevisionMixin, FormView):

    template_name = 'member_edit.html'
    form_class = MemberForm
    success_url = '/.../'

    ##############################################

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

####################################################################################################

class MemberSearchForm(Form):

    query = CharField(
        label='', # _('Query'),
        help_text=_('Enter part of a name or a license ID'),
        required=False,
        initial='',
    )

    ##############################################

    def filter_by(self):

        query = self.cleaned_data['query']

        try:
            _ = int(query)
            return Q(license_id=query)
        except ValueError:
            return Q(user__last_name__startswith=query.upper()) # Fixme: due to upper case

####################################################################################################

# @login_required is done in urls
class MemberListView(FormMixin, ListView):

    template_name = 'member/index.html'

    # ListView
    model = Member
    queryset = Member.objects.all().order_by('user__last_name')
    context_object_name = 'members' # else object_list
    paginate_by = None

    # FormMixin
    form_class = MemberSearchForm

    ##############################################

    def get_form_kwargs(self):

        # FormMixin: Build the keyword arguments required to instantiate the form.
        # cf. django/views/generic/edit.py FormMixin

        # Called by self.get_form
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None,
        }
        # {'initial': {}, 'data': None, 'prefix': None}
        # {'data': <QueryDict: {'csrfmiddlewaretoken': ['K...u'], 'name': ['apr']}>, 'initial': {}, 'prefix': None}
        return kwargs

    ##############################################

    def get(self, request, *args, **kwargs):

        # cf. django/views/generic/list.py BaseListView

        self.object_list = self.get_queryset()

        form = self.get_form()
        if form.is_valid():
            self.object_list = self.object_list.filter(form.filter_by())

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

####################################################################################################

@login_required
def member_as_csv(request):

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)

    # User = Member.user.field.related_model

    header = [field_to_verbose_name(field) for field in (
        # Identify
        'User.username',
        'User.last_name', 'User.first_name',
        'Member.birth_date', 'Member.sex',
        # License
        'Member.license_id', 'Club.name',
        # Adresse
        'Member.address', 'FrenchCity.zip_code', 'FrenchCity.libelle', 'FrenchCity.ligne_5',
        # Contact',
        'User.email',
        'Member.phone_mobile', 'Member.phone_home', 'Member.phone_work',
        # Adhesion
        'ClubMember.group',
        'ClubMember.registration_year',
        'ClubMember.social_discount',
    )]

    writer.writerow(header)
    for member in Member.objects.order_by('user__last_name', 'user__first_name'):
        user = member.user
        city = member.city
        club_member = member.club_member
        fields = [
            # Identify
            user.username,
            user.last_name, user.first_name,
            member.birth_date, # Fixme: format ???
            member.get_sex_display(),
            # License
            member.license_id, member.license_club.name,
        ]
        if city is not None:
            fields += [
                # Adresse
                member.address, city.zip_code, city.libelle, city.ligne_5,
            ]
        else:
            fields += [None]*4
        fields += [
            # Contact,
            user.email,
            member.phone_mobile, member.phone_home, member.phone_work,
            # Adhesion
            club_member.get_group_display(),
            club_member.registration_year,
            club_member.social_discount,
        ]
        writer.writerow(fields)

    return response

####################################################################################################

@login_required
def details(request, member_id):

    member = get_object_or_404(Member, pk=member_id)

    return render(request, 'member/details.html', {'member': member})

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            messages.success(request, _("Member créé avec succès."))
            return HttpResponseRedirect(reverse('member.details', args=[member.pk]))
        else:
            messages.error(request, _("Des informations sont manquantes ou incorrectes"))
    else:
        form = MemberForm()

    return render(request, 'member/create.html', {'form': form})

####################################################################################################

@login_required
@reversion.views.create_revision(manage_manually=False, using=None, atomic=True)
def update(request, member_id):

    member = get_object_or_404(Member, pk=member_id)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save()
            return HttpResponseRedirect(reverse('member.details', args=[member.pk]))
    else:
        form = MemberForm(instance=member)

    return render(request, 'member/create.html', {'form': form, 'update': True, 'member': member})

####################################################################################################

@login_required
def delete(request, member_id):

    member = get_object_or_404(Member, pk=member_id)
    messages.success(request, _("Member «{0.name}» supprimé").format(member))
    member.delete()

    return HttpResponseRedirect(reverse('member.index'))
