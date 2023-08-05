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
from concurrent.futures.thread import ThreadPoolExecutor

from . import Notifier


class ThreadedNotifier(Notifier):
    def __init__(self, pool_size=10):
        assert pool_size >= 2, "requires pool_size >= 2"
        self.pool = ThreadPoolExecutor(max_workers=pool_size)

    def notify(self, event, subscribers):
        def dispatch():
            for subscriber in subscribers:
                self.pool.submit(subscriber, event)
        self.pool.submit(dispatch)
