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

import asyncio
import logging

import uvloop

from . import Notifier

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


logger = logging.getLogger(__name__)


class AsyncNotifier(Notifier):

    def notify(self, event, subscribers):
        async def f():
            for s in subscribers:
                try:
                    s(event)
                except BaseException:
                    logger.exception('exception during notification')
        return asyncio.run(f())
