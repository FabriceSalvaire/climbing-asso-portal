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

from django.contrib import messages
from django.db.models import Q
from django.forms import ModelForm, Form, CharField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

# from django.shortcuts import render
from django.views.generic.edit import FormView

# from django.contrib.auth.decorators import login_required
from account.decorators import login_required

import reversion
from reversion.views import RevisionMixin

from ..forms import MemberForm
from ..models import Member, ClubMember

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
