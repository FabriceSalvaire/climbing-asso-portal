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
from django.core.serializers import serialize
from django.db.models import Count, Q
from django.forms import ModelForm, Form, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_control
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, FormView

# from django.contrib.auth.decorators import login_required
from account.decorators import login_required

import reversion
from reversion.views import RevisionMixin

import numpy as np

from IntervalArithmetic import Interval

from ClimbingAssoPortalTools.Plot import MatplolibPlot
from ClimbingAssoPortalTools.Statistics.Binning import Binning1D
from ClimbingAssoPortalTools.Statistics.Histogram import Histogram

from ..constants import ONE_HOUR
from ..forms import MemberForm
from ..models import ClubMember, FrenchCity, Member
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

# Fixme: @cache_result
def generate_age_histogram():

    binning = Binning1D(Interval(10, 80), bin_width=2)
    histograms = {
        'm': Histogram(binning),
        'f': Histogram(binning),
    }

    for member in Member.objects.all():
        if member.sex in histograms.keys(): # Fixme: s ???
            histograms[member.sex].fill(member.age)

    return histograms

####################################################################################################

# @cache_result
def generate_age_histogram_plot(show_error=False):

    histograms = generate_age_histogram()

    plot = MatplolibPlot(aspect_ratio=4/3)
    plot.figure.tight_layout()
    axes = plot.subplot()

    FONTSIZE = 17
    axes.tick_params(axis='both', which='major', labelsize=FONTSIZE)

    axes.set_title(_('Age Histogram'), fontsize=FONTSIZE*1.2)

    interval = histograms['f'].binning.interval
    axes.set_xticks(np.arange(interval.inf, interval.sup, 5))

    axes.grid()

    WIDTH = 2

    # https://matplotlib.org/_images/named_colors.png
    sex_color = {
        'm': 'dodgerblue',
        'f': 'deeppink',
    }

    for sex, histogram in histograms.items():
        x_values, y_values, x_errors, y_errors = histogram.to_graph()
        if show_error:
            axes.errorbar(x_values, y_values, xerr=x_errors, yerr=y_errors, fmt='o', color=sex_color[sex], alpha=.5)
        else:
            axes.bar(x_values, y_values, width=WIDTH , edgecolor='white', color=sex_color[sex], alpha=.5)

    if show_error:
        x = .6
        y = .95
        y_step = .05
        for sex, in sorted(histograms.keys()):
            histogram = histograms[sex]
            sex_text = _('Female') if sex == 'f' else 'Male'
            axes.text(
                x, y,
                _('Number of {}s {}').format(sex_text, int(histogram.integral)),
                transform = axes.transAxes,
            )
            y -= y_step
            axes.text(
                x, y,
                _('Mean {} {:.1f} +- {:.1f}').format(sex_text, histogram.mean, histogram.standard_deviation),
                transform = axes.transAxes,
            )
            y -= y_step
            axes.text(
                x, y,
                _('Kurtosis {} {:.2f}').format(sex_text, histogram.kurtosis),
                transform = axes.transAxes,
            )
            y -= y_step
            axes.text(
                x, y,
                _('Skewness {} {:.2f}').format(sex_text, histogram.skew),
                transform = axes.transAxes,
            )
            y -= y_step * 2

    return plot.to_svg()

####################################################################################################

def _age_historgam(request, show_error):

    histogram = generate_age_histogram_plot(show_error)
    svg_data = histogram.div
    return HttpResponse(svg_data, content_type='image/svg+xml')


@cache_control(max_age=ONE_HOUR)
@login_required
def age_histogram_svg(request):
    return _age_historgam(request, show_error=False)

@cache_control(max_age=ONE_HOUR)
@login_required
def age_histogram_error_svg(request):
    return _age_historgam(request, show_error=True)

####################################################################################################

@login_required
def age_histogram_csv(request):

    histograms = generate_age_histogram()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)

    header = (
        _('Sex'),
        _('Age Class Inf'),
        _('Age Class Sup'),
        _('Count'),
        _('Statistical Count Error'),
    )
    writer.writerow(header)

    for sex, histogram in histograms.items():
        binning = histogram.binning
        for i in binning.bin_iterator(xflow=True):
            interval = binning.bin_interval(i)
            fields = (
                sex,
                interval.inf,
                interval.sup,
                histogram.accumulator[i],
                histogram.get_bin_error(i),
            )
            writer.writerow(fields)

    return response

####################################################################################################

@login_required
def member_statistics(request):
    return render(request, 'member/statistics.html', {})

####################################################################################################

@login_required
def member_city_geojson(request):

    query = FrenchCity.objects.annotate(member_count=Count('member'))
    query = query.filter(member_count__gt=0).order_by('zip_code')

    json_data = serialize(
        'geojson_ext',
        query,
        # fields=('name', 'zip_code', 'libelle', 'ligne_5', 'member_count',),
        fields=('as_address', 'member_count',),
        geometry_field='coordinate',
    )

    return HttpResponse(json_data, content_type='application/json')

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
