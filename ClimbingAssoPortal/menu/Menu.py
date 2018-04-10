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

class Menu:

    ##############################################

    def __init__(self,
                 name=None,
                 title=None,
                 icon=None,
                 url=None,
                 login_required=False,
                 group_required=None,
                 parent=None,
                 match=None,
                 childs=[],
    ):

        self._name = name
        self._title = title
        self._icon = icon
        self._url = url

        self._login_required = login_required
        self._group_required = group_required

        self._match = match

        self._parent = parent
        self._childs = list(childs)

        if parent is not None:
            parent.add_item(self)

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def icon(self):
        return self._icon

    @property
    def url(self):
        return self._url

    ##############################################

    @property
    def login_required(self):
        return self._login_required

    @property
    def group_required(self):
        return self._group_required

    ##############################################

    def __bool__(self):
        return self._title

    ##############################################

    @property
    def match_url(self):
        return self._match

    def match(self, url):
        rc = url.startswith(self._match)
        return rc

    ##############################################

    @property
    def parent(self):
        return self._parent

    @property
    def as_childs(self):
        return bool(self._childs)

    def __len__(self):
        return len(self._childs)

    def __iter__(self):
        return iter(self._childs)

    def __getitem__(self, _slice):
        return self._childs[_slice]

    def __add__(self, item):
        self.add_item(item)

    def add_item(self, item):
        self._childs.append(item)
