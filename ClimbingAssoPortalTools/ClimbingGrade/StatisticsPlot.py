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
from io import StringIO

import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# WSGI Hang
# print(bokeh ...)
# # from bokeh.plotting import figure
# from bokeh.embed import components
# from bokeh.charts import Bar
# from bokeh.charts.attributes import CatAttr
# print(bokeh done)

####################################################################################################

class BokehPlot:

    ##############################################

    def __init__(self, *args, **kwargs):

        script, div = components(*args, **kwargs)
        self.script = script
        self.div = div

####################################################################################################

class SvgPlot:

    ##############################################

    def __init__(self, svg):

        self.script = ''
        self.div = svg

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

            # engine = self._make_bokeh_barchart
            engine = self._make_svg_barchart

            self._histogram = engine(labels, counts, title)
            self._cumulative = engine(
                labels,
                cumulative_counts,
                cumulative_title,
                percent=True,
            )
            self._inverse_cumulative = engine(
                labels,
                inverse_cumulative_counts,
                inverse_cumulative_title,
                percent=True,
            )
        else:
            self._plot = None
            self._cumulative = None
            self._inverse_cumulative = None

    ##############################################

    @property
    def histogram(self):
        return self._histogram

    @property
    def cumulative(self):
        return self._cumulative

    @property
    def inverse_cumulative(self):
        return self._inverse_cumulative

    ##############################################

    def __getitem__(self, plot):

        if plot == 'histogram':
            return self._histogram
        elif plot == 'cumulative':
            return self._cumulative
        elif plot == 'inverse_cumulative':
            return self._inverse_cumulative
        else:
            raise ValueError

    ##############################################

    def __hash__(self):

        return hashlib.sha1(str(self._histogram.domain))

    ##############################################

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

    ##############################################

    def _make_svg_barchart(self, labels, counts, title, percent=False):

        dpi = 100
        figure_width = 1000 / dpi
        aspect_ratio = 16 / 9
        figure_height = figure_width / aspect_ratio

        figure = Figure(figsize=(figure_width, figure_height), dpi=dpi, facecolor='white')
        axes = figure.add_subplot(1, 1, 1)
        y = counts
        if percent:
            y *= 100
        x = np.arange(len(y))
        width = .5
        bar_chart = axes.bar(x, y, width=width, color='r', edgecolor='white')

        axes.set_title(title, fontsize=20)

        axes.set_xticks(x + width/2)
        axes.xaxis.set_tick_params(width=0)
        axes.set_xticklabels(labels, rotation=45, fontsize=15)

        if percent:
            major_ticks = np.arange(0, 101, 10)
            axes.set_yticks(major_ticks)
            # axes.set_yticks(minor_ticks, minor=True)
        else:
            major_ticks = np.arange(0, y[y.argmax()] + 1, 5)
            axes.set_yticks(major_ticks)
            # axes.set_yticks(minor_ticks, minor=True)
        axes.set_ylabel('%' if percent else '')
        axes.grid(axis='y')

        canvas = FigureCanvas(figure)
        image_data = StringIO()
        canvas.print_figure(image_data, format='svg')
        svg = image_data.getvalue()
        svg = svg[svg.find('<svg'):]

        return SvgPlot(svg)
