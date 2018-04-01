####################################################################################################
#
# Climbing Grade
# Copyright (C) 2015 Fabrice Salvaire
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

import hashlib

import numpy as np

from ..Plot import MatplolibPlot

####################################################################################################

class PlotAbc:

    WIDTH = .75
    FONTSIZE = 17

    ##############################################

    def __init__(self, labels, title):

        self._plot = MatplolibPlot(aspect_ratio=4/3)
        axes = self._plot.subplot()
        self._axes = axes

        self._plot.figure.tight_layout(pad=4)
        self._axes.tick_params(axis='both', which='major', labelsize=self.FONTSIZE)

        axes.set_title(title, fontsize=self.FONTSIZE*1.2)

        self._x = np.arange(len(labels))
        axes.set_xticks(self._x)
        axes.xaxis.set_tick_params(width=0)
        axes.set_xticklabels(labels, rotation=45)

        axes.grid(axis='y')

    ##############################################

    @property
    def axes(self):
        return self._axes

    ##############################################

    @property
    def plot(self):
        return self._plot.to_svg()

    ##############################################

    def barchart(self, y, color, alpha=1):

        self._axes.bar(self._x, y, width=self.WIDTH, color=color, alpha=alpha, edgecolor='white')

####################################################################################################

class GradeBarchart(PlotAbc):

    ##############################################

    def __init__(self, labels, y, title):

        super().__init__(labels, title)

        self.barchart(y, color='dodgerblue')

        major_ticks = np.arange(0, y[y.argmax()] + 1, 5)
        self.axes.set_yticks(major_ticks)

####################################################################################################

class GradeCumulative(PlotAbc):

    ##############################################

    def __init__(self, labels, **kwargs):

        title = kwargs['cumulative_title']
        super().__init__(labels, title)

        for graph in ('cumulative', 'inverse_cumulative'):
            y = kwargs[graph]
            y *= 100
            # https://matplotlib.org/examples/color/named_colors.html
            if graph == 'cumulative':
                color = 'dodgerblue'
            else:
                color = 'chocolate'
            self.barchart(y, color=color, alpha=.5)

        major_ticks = np.arange(0, 101, 10)
        self.axes.set_yticks(major_ticks)
        self.axes.set_ylabel('%', fontsize=self.FONTSIZE)

####################################################################################################

class FrenchGradeHistogramPlot:

    ##############################################

    def __init__(self, histogram, title, cumulative_title, inverse_cumulative_title):

        histogram = histogram
        title = title
        cumulative_title = cumulative_title
        inverse_cumulative_title = inverse_cumulative_title

        grade_counters = histogram.domain
        if grade_counters:
            labels = [str(grade_counter) for grade_counter in grade_counters]
            counts = np.array([grade_counter.count for grade_counter in grade_counters])
            cumulative_counts = counts.cumsum() / counts.sum()
            inverse_cumulative_counts = np.ones(len(counts))
            inverse_cumulative_counts[1:] = (1 - cumulative_counts)[:-1]

            self._histogram = GradeBarchart(labels, counts, title).plot
            self._cumulative = GradeCumulative(
                labels,
                cumulative=cumulative_counts,
                inverse_cumulative=inverse_cumulative_counts,
                cumulative_title=cumulative_title,
                inverse_cumulative_title=inverse_cumulative_title,
            ).plot
        else:
            self._plot = None
            self._cumulative = None

    ##############################################

    @property
    def histogram(self):
        return self._histogram

    @property
    def cumulative(self):
        return self._cumulative

    ##############################################

    def __getitem__(self, plot):

        if plot == 'histogram':
            return self._histogram
        elif plot == 'cumulative':
            return self._cumulative
        else:
            raise ValueError

    ##############################################

    def __hash__(self):

        return hashlib.sha1(str(self._histogram.domain))

####################################################################################################

    # def _make_bokeh_barchart(self, labels, counts, title):

    #     # Workaround to don't sort labels
    #     label = CatAttr(df=data, columns='labels', sort=False)
    #     bar = Bar(data,
    #               values='counts', label=label,
    #               title=title,
    #               xlabel='',
    #               ylabel='',
    #               plot_width=300,
    #               plot_height=200,
    #               responsive=True,
    #               tools='',
    #               toolbar_location=None,
    #     )
    #     return BokehPlot(bar)
