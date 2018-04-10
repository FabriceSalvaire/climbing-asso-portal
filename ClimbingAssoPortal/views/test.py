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

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView

from django_select2 import forms as select2_forms

# from django.contrib.auth.decorators import login_required
from account.decorators import login_required

from .. import models as app_models

####################################################################################################

class Select2Form(forms.Form):

    query = forms.ChoiceField(
        widget=select2_forms.ModelSelect2Widget(
            model=app_models.Member,
            search_fields=['user__last_name__startswith'],
            # ??? attrs={'width': '200px'},
        ),
    )

####################################################################################################

# <select name="query" required="" id="id_query" data-allow-clear="false" data-minimum-input-length="0"
#         class="django-select2 select2-hidden-accessible" tabindex="-1" aria-hidden="true">
#   <option value="" selected="">---------</option>
#   <option value="2400">...</option>
# </select>

@login_required
def test_django_selet2(request):

    if request.method == 'POST':
        print('test_django_selet2 POST', request)
        # create a form instance and populate it with data from the request:
        form = Select2Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('test_django_selet2 POST form is valid')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('test.index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        print('test_django_selet2 GET', request)
        form = Select2Form()

    return render(request, 'devel/test/django_select2.html', {'form': form})

####################################################################################################

class TemplateFormView(FormView):
    template_name = 'devel/test/django_select2.html'
    form_class = Select2Form
