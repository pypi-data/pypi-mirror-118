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
from .notifier.threaded_notifier import ThreadedNotifier
from .subject import Choice, R, Reactive, Splitter
from .utils import AcyclicalDiGraph


class Context(object):
    def __init__(self, notifier=None):
        self.notifier = ThreadedNotifier() if notifier is None else notifier
        self.g = None

    def new(self, clazz, *args, **kwargs):
        kwargs['context'] = self
        return clazz(*args, **kwargs)

    def reactive(self, *sources):
        return Reactive(*sources, context=self)

    def splitter(self, *sources):
        return Splitter(*sources, context=self)

    def choice(self, *sources, key_extractor, target_dict):
        return Choice(*sources, key_extractor=key_extractor,
                      target_dict=target_dict, context=self)

    def r(self, value=None):
        return R(value=value, context=self)

    def __enter__(self):
        self.g = AcyclicalDiGraph()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.g.clear()
        return False
