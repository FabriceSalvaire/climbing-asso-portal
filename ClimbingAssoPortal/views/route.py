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
from django.forms import Form, CharField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_control
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

# from django.shortcuts import render
from django.views.generic.edit import FormView

# from django.contrib.auth.decorators import login_required
from account.decorators import login_required

import reversion
from reversion.views import RevisionMixin

from ClimbingAssoPortalTools.CacheTools import cache_result
from ClimbingAssoPortalTools.ClimbingGrade import FrenchGrade
from ClimbingAssoPortalTools.ClimbingGrade.Statistics import FrenchGradeHistogram
from ClimbingAssoPortalTools.ClimbingGrade.StatisticsPlot import FrenchGradeHistogramPlot

from ..constants import ONE_HOUR
from ..forms.route import RouteForm
from ..models import Route

####################################################################################################

@cache_result
def generate_route_histogram():

    histogram = FrenchGradeHistogram()

    for route in Route.objects.all():
        grade = route.grade
        if grade:
            if grade == 'ENF':
                grade = '4a'
            grade = FrenchGrade(grade)
            histogram.increment(grade)

    histogram_plot = FrenchGradeHistogramPlot(
        histogram,
        title=_('Route Grades'),
        cumulative_title=_('Cumulative Histogram of the Route Grades'),
        inverse_cumulative_title=_('Inverse Cumulative Histogram of the Route Grades'),
    )

    return histogram_plot

####################################################################################################

def _route_historgam(request, plot):

    histogram = generate_route_histogram()
    svg_data = histogram[plot].div
    return HttpResponse(svg_data, content_type='image/svg+xml')


# Fixme: browser cache ???
@cache_control(max_age=ONE_HOUR)
@login_required
def route_historgam_svg(request):
    return _route_historgam(request, plot='histogram')

@cache_control(max_age=ONE_HOUR)
@login_required
def route_cumulative_histogram_svg(request):
    return _route_historgam(request, plot='cumulative')

####################################################################################################

class RouteFormView(RevisionMixin, FormView):

    template_name = 'route_edit.html'
    form_class = RouteForm
    success_url = '/.../'

    ##############################################

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

####################################################################################################

class RouteSearchForm(Form):

    name = CharField(label=_('Name'), required=False, initial='')

    ##############################################

    def filter_by(self):
        # Fixme:
        return {'name__icontains': self.cleaned_data['name']}

####################################################################################################

class RouteListView(FormMixin, ListView):

    template_name = 'route/index.html'

    # ListView
    model = Route
    queryset = Route.objects.all().order_by('line_number')
    context_object_name = 'routes' # else object_list
    paginate_by = None

    # FormMixin
    form_class = RouteSearchForm

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
def details(request, route_id):

    route = get_object_or_404(Route, pk=route_id)

    return render(request, 'route/details.html', {'route': route})

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.save()
            messages.success(request, _("Route créé avec succès."))
            return HttpResponseRedirect(reverse('route.details', args=[route.pk]))
        else:
            messages.error(request, _("Des informations sont manquantes ou incorrectes"))
    else:
        form = RouteForm()

    return render(request, 'route/create.html', {'form': form})

####################################################################################################

@login_required
@reversion.views.create_revision(manage_manually=False, using=None, atomic=True)
def update(request, route_id):

    route = get_object_or_404(Route, pk=route_id)

    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            route = form.save()
            return HttpResponseRedirect(reverse('route.details', args=[route.pk]))
    else:
        form = RouteForm(instance=route)

    return render(request, 'route/create.html', {'form': form, 'update': True, 'route': route})

####################################################################################################

@login_required
def delete(request, route_id):

    route = get_object_or_404(Route, pk=route_id)
    messages.success(request, _("Route «{0.name}» supprimé").format(route))
    route.delete()

    return HttpResponseRedirect(reverse('route.index'))
