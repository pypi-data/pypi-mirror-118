#
#     QuantLET-core - Core componenents in QuantLET
#
#     Copyright (C) 2006 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import networkx as nx


class CycleError(Exception):
    pass


class NoPathError(Exception):
    pass


class AcyclicalDiGraph(nx.DiGraph):
    def add_edge(self, u_of_edge, v_of_edge, **attr):
        super().add_edge(u_of_edge, v_of_edge, **attr)
        try:
            cycles = nx.find_cycle(self, orientation='original')
            self.remove_edge(u_of_edge, v_of_edge)
            raise CycleError(u_of_edge, v_of_edge, cycles)
        except nx.NetworkXNoCycle:
            pass

    def shortest_path(self, source, target=None):
        if not nx.has_path(self, source, target):
            raise NoPathError(source, target)
        return nx.shortest_path(self, source=source, target=target)
