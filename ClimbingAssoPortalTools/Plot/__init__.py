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

from io import StringIO

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

class MatplolibPlot:

    ##############################################

    def __init__(self, aspect_ratio=16/9):

        dpi = 100
        figure_width = 1000 / dpi
        figure_height = figure_width / aspect_ratio

        self._figure = Figure(
            figsize=(figure_width, figure_height),
            dpi=dpi,
            facecolor='white',
        )

    ##############################################

    @property
    def figure(self):
        return self._figure

    ##############################################

    def subplot(self):

        self._axes = self._figure.add_subplot(1, 1, 1)

        return self._axes

    ##############################################

    def to_svg(self):

        canvas = FigureCanvas(self._figure)
        image_data = StringIO()
        canvas.print_figure(image_data, format='svg')
        svg = image_data.getvalue()
        svg = svg[svg.find('<svg'):]

        return SvgPlot(svg)

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
