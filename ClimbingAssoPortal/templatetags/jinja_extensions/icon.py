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

from django.conf import settings
from django.utils import translation

from jinja2 import lexer, nodes, Markup
from jinja2.ext import Extension

####################################################################################################

class Icon(Extension):

    tags = set(['icon'])

    ##############################################

    def parse(self, parser):

        stream = parser.stream

        lineno = stream.expect('name:icon').lineno
        name = stream.expect('string').value
        additional_classes = []
        while not stream.current.test('block_end'):
            additional_classes = stream.expect('string').value

        if '.' in name:
            domain, name = name.split('.')
        elif name.startswith('fa-'):
            domain = 'fa'
        else:
            parser.fail('invalid icon name {}'.format(name), lineno)

        call = self.call_method(
            '_render',
            [
                nodes.Const(domain),
                nodes.Const(name),
                nodes.List(additional_classes),
            ],
            lineno=lineno
        )

        return nodes.Output([nodes.MarkSafe(call)])

    ##############################################

    def _render(self, domain, name, additional_classes):

        if domain in ('fa', 'fas', 'far', 'fab'):
            html_code = '<i class="{} {} {}"></i>'.format(domain, name, ' '.join(additional_classes))

        return Markup(html_code)
