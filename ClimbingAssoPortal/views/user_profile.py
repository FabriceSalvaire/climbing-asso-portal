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
from django.urls import reverse
from django.forms import ModelForm, Form, CharField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

# from django.shortcuts import render
from django.views.generic.edit import FormView

# from django.contrib.auth.decorators import login_required
from account.decorators import login_required

import reversion
from reversion.views import RevisionMixin

from ..forms import UserProfileForm
from ..models import UserProfile

####################################################################################################

class UserProfileFormView(RevisionMixin, FormView):

    template_name = 'user_profile_edit.html'
    form_class = UserProfileForm
    success_url = '/.../'

    ##############################################

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

####################################################################################################

class UserProfileSearchForm(Form):

    name = CharField(label=_('Name'), required=False, initial='')

    ##############################################

    def filter_by(self):
        # Fixme:
        return {'user__last_name__icontains': self.cleaned_data['name']}

####################################################################################################

class UserProfileListView(FormMixin, ListView):

    template_name = 'user_profile/index.html'

    # ListView
    model = UserProfile
    queryset = UserProfile.objects.all().order_by('user__last_name')
    context_object_name = 'user_profiles' # else object_list
    paginate_by = None

    # FormMixin
    form_class = UserProfileSearchForm

    ##############################################

    def get_form_kwargs(self):

        # FormMixin: Build the keyword arguments required to instantiate the form.
        # cf. django/views/generic/edit.py FormMixin

        # Called by self.get_form
        kwargs = {'initial': self.get_initial(),
                  'prefix': self.get_prefix(),
                  'data': self.request.GET or None}
        # {'initial': {}, 'data': None, 'prefix': None}
        # {'data': <QueryDict: {'csrfmiddlewaretoken': ['K...u'], 'name': ['apr']}>, 'initial': {}, 'prefix': None}
        return kwargs

    ##############################################

    def get(self, request, *args, **kwargs):

        # cf. django/views/generic/list.py BaseListView

        self.object_list = self.get_queryset()
        print(self.object_list)

        form = self.get_form()
        if form.is_valid():
            self.object_list = self.object_list.filter(**form.filter_by())

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

####################################################################################################

@login_required
def details(request, user_profile_id):

    user_profile = get_object_or_404(UserProfile, pk=user_profile_id)

    return render(request, 'user_profile/details.html', {'user_profile': user_profile})

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.save()
            messages.success(request, _("UserProfile créé avec succès."))
            return HttpResponseRedirect(reverse('user_profile.details', args=[user_profile.pk]))
        else:
            messages.error(request, _("Des informations sont manquantes ou incorrectes"))
    else:
        form = UserProfileForm()

    return render(request, 'user_profile/create.html', {'form': form})

####################################################################################################

@login_required
@reversion.views.create_revision(manage_manually=False, using=None, atomic=True)
def update(request, user_profile_id):

    user_profile = get_object_or_404(UserProfile, pk=user_profile_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save()
            return HttpResponseRedirect(reverse('user_profile.details', args=[user_profile.pk]))
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profile/create.html', {'form': form, 'update': True, 'user_profile': user_profile})

####################################################################################################

@login_required
def delete(request, user_profile_id):

    user_profile = get_object_or_404(UserProfile, pk=user_profile_id)
    messages.success(request, _("UserProfile «{0.name}» supprimé").format(user_profile))
    user_profile.delete()

    return HttpResponseRedirect(reverse('user_profile.index'))
