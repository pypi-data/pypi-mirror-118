#
#     Reactives - a small, simple, and fast framework for reactive programming
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
#


import networkx as nx


class UndoOnExcept(object):
    """Context manager to rollback single operations on exception
    """

    def __init__(self, rollback, suppress=False):
        self.rollback = rollback
        self.suppress = suppress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
        return self.suppress


class AcyclicalDiGraph(nx.DiGraph):
    def add_edge(self, u_of_edge, v_of_edge, **attr):
        super().add_edge(u_of_edge, v_of_edge, **attr)
        try:
            cycles = nx.find_cycle(self, orientation='original')
            self.remove_edge(u_of_edge, v_of_edge)
            raise ValueError(
                f'edge ({u_of_edge},{v_of_edge}) caused a cycle: {cycles}')
        except nx.NetworkXNoCycle:
            pass

    def shortest_path(self, source, target=None):
        if not nx.has_path(self, source, target):
            raise nx.NetworkXNoPath(source, target)
        return nx.shortest_path(self, source=source, target=target)
