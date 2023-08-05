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
import inspect
import logging
import operator as op
import uuid
import weakref
from abc import ABC
from inspect import signature
from operator import (add, and_, concat, contains, delitem, eq, floordiv, ge,
                      getitem, gt, iadd, iand, iconcat, ifloordiv, ilshift,
                      imatmul, imod, imul, inv, ior, ipow, irshift, isub,
                      itruediv, ixor, le, lshift, lt, matmul, mod, mul, ne,
                      not_, or_, pow, rshift, sub, truediv, xor)
from typing import NamedTuple

from .utils import UndoOnExcept

logger = logging.getLogger(__name__)


class Event(NamedTuple):
    subject: object
    value: object
    previous_value: object


class GuardException(Exception):
    pass


class DropOutException(Exception):
    pass


def guard(f, message=None):
    def g(event):
        if not f(event):
            raise GuardException('%s: %s in %s' %
                                 (message if message is not None else '',
                                  event,
                                  inspect.getsourcelines(f)[0][0].strip()))
        return event
    return g


def dropout_if(f):
    def g(event):
        if f(event):
            raise DropOutException()
        return event
    return g


class Node(object):
    def __init__(self, reactive):
        self.reactive = weakref.proxy(reactive)


def _tracing(f):
    def wrapper(*args, **kwargs):
        logger.debug(f'>>{args} {kwargs}')
        v = f(*args, **kwargs)
        logger.debug(f'<<{v}')
        return v
    return wrapper


def _notify(functions, value, drop_exceptions=False):
    for f in functions:
        try:
            f(value)
        except BaseException as e:
            if not drop_exceptions:
                if isinstance(e, DropOutException):
                    return
                else:
                    raise e
            else:
                logger.exception(
                    f'dropped exception while calling {repr(f)}({value})')


def _notify_propagate(functions, value):
    for f in functions:
        value = f(value)
    return value


def _notify_propagate_set(functions, value, container):
    container._value = value
    for f in functions:
        value = f(value)
        container._value = value
    return value


class Reactive(ABC):
    def __init__(self, *sources, label=None, context=None):
        assert context is not None
        self._context = context
        self._label = label if label is not None else uuid.uuid4().hex
        self._prereqs = list()
        self._postreqs = list()
        self._subscriptions = list()
        self._previous_value = None
        self._sources = list()
        self.node = Node(self)
        self.link(*sources)

    @property
    def value(self):
        raise ValueError('stateless')

    @value.setter
    def value(self, value):
        self.apply(value)

    @property
    def label(self):
        return self._label

    @property
    def previous_value(self):
        return self._previous_value

    def is_valid(self):
        return all([s.is_valid() for s in self._sources])

    def pre(self, *values):
        self._prereqs += values

    def post(self, *values):
        self._postreqs += values

    def subscribe(self, *values):
        self._subscriptions += values

    def link_reverse(self, *other):
        """add a reverse link from other to self.
        """
        for t in other:
            t.link(self)

    def link(self, *other):
        """add self as a pre-requisite to a reaction on other,
        or, self is a reactive dependency on other.
        other will only react if self (and all its chained
        downstream pre-requisites) allow.
        """
        assert self._context.g is not None, ("context not initialized or not "
                                             "within a with block")
        self._sources += other
        for s in other:
            self._context.g.add_edge(s.node, self.node)
            with UndoOnExcept(lambda: self._context.g.remove_edge(s.node,
                                                                  self.node)):
                s.pre(self.cycle)

    # @_tracing
    def cycle(self, event, propagate=False):
        event = event if propagate else Event(
            subject=self,
            value=event.value,
            previous_value=self._previous_value
        )
        _notify(self._prereqs, event, drop_exceptions=False)
        _notify(self._postreqs, event, drop_exceptions=True)
        self._context.notifier.notify(subscribers=self._subscriptions,
                                      event=event)
        self._previous_value = event.value

    def apply(self, value):
        self.cycle(Event(
            subject=self,
            value=value,
            previous_value=self._previous_value), propagate=True)


class Splitter(Reactive):
    pass


class Choice(Reactive):
    def __init__(self, *sources, key_extractor, target_dict, label=None,
                 context=None):
        super().__init__(*sources, label=label, context=context)

        def dispatch(value):
            r = target_dict[key_extractor(value)]
            return r.cycle(value)

        self.pre(
            dispatch
        )


class F(Reactive):
    def __init__(self, *sources, function, label=None, context=None):
        super().__init__(*sources, label=label, context=context)
        self._function = function
        self._value_function_exception = None
        self._previous_value = self.value

    @property
    def value_function_exception(self):
        return self.value_function_exception

    @property
    def value(self):
        try:
            return self._function()
        except BaseException as e:
            self._value_function_exception = e

    # @_tracing
    def cycle(self, _):
        event = Event(subject=self,
                      value=self.value,
                      previous_value=self._previous_value)
        _notify(self._prereqs, event, drop_exceptions=False)
        _notify(self._postreqs, event, drop_exceptions=True)
        self._context.notifier.notify(subscribers=self._subscriptions,
                                      event=event)
        self._previous_value = self.value


class Pipeline(Reactive):
    def __init__(self, *sources, functions, label=None, context=None):
        super().__init__(*sources, label=label, context=context)
        self.functions = functions

    def _pipeline(self, item):
        for f in self.functions:
            item = f(item)
        return item

    def cycle(self, event, propagate=True):
        super().cycle(Event(subject=self, value=self._pipeline(
            event.value), previous_value=self._previous_value), propagate=propagate)


class Value(F):
    def __init__(self, value=None, label=None, context=None):
        super().__init__(function=lambda: self._value, label=label,
                         context=context)
        self._value = value
        self._cycling = False

    @ property
    def value(self):
        return super().value

    def is_valid(self):
        return self._value is not None

    @ value.setter
    def value(self, value):
        self.apply(value)

    def apply(self, value):
        if self._cycling:
            raise ValueError(
                f'value setting not allowed while reacting {repr(self)}')
        self._cycling = True
        previous_value = self._previous_value
        self._previous_value = self._value
        self._value = value
        try:
            self.cycle(None)
        except BaseException as e:
            self._value = self._previous_value
            self._previous_value = previous_value
            raise e
        finally:
            self._cycling = False

    # @_tracing
    def cycle(self, _, propagate=False):
        event = Event(
            subject=self, value=self._value,
            previous_value=self._previous_value)
        _notify(self._prereqs, event, drop_exceptions=False)
        try:
            _notify(self._postreqs, event, drop_exceptions=True)
            self._context.notifier.notify(
                subscribers=self._subscriptions,
                event=event)
        except BaseException:
            logging.exception(
                f'dropped unexpected exception on {event} '
                f'@ {repr(self)}')


class Numeric(F):
    def __init__(self, *sources, function, label, context):
        super().__init__(*sources, function=function, context=context)

    def __lt__(self, other):
        return F(self, other, function=lambda: lt(
            self.value, other.value), context=self._context)

    def __le__(self, other):
        return F(self, other, function=lambda: le(
            self.value, other.value), context=self._context)

    def __eq__(self, other):
        return F(self, other, function=lambda: eq(
            self.value, other.value), context=self._context)

    def __ne__(self, other):
        return F(self, other, function=lambda: ne(
            self.value, other.value), context=self._context)

    def __ge__(self, other):
        return F(self, other, function=lambda: ge(
            self.value, other.value), context=self._context)

    def __gt__(self, other):
        return F(self, other, function=lambda: gt(
            self.value, other.value), context=self._context)

    def __not__(self):
        return F(self, function=lambda: not_(
            self.value), context=self._context)

    def __add__(self, other):
        return F(self, other, function=lambda: add(
            self.value, other.value), context=self._context)

    def __and__(self, other):
        return F(self, other, function=lambda: and_(
            self.value, other.value), context=self._context)

    def __floordiv__(self, other):
        return F(self, other, function=lambda: floordiv(
            self.value, other.value), context=self._context)

    def __inv__(self):
        return F(self, function=lambda: inv(
            self.value), context=self._context)

    def __lshift__(self, other):
        return F(self, other, function=lambda: lshift(
            self.value, other.value), context=self._context)

    def __mod__(self, other):
        return F(self, other, function=lambda: mod(
            self.value, other.value), context=self._context)

    def __mul__(self, other):
        return F(self, other, function=lambda: mul(
            self.value, other.value), context=self._context)

    def __matmul__(self, other):
        return F(self, other, function=lambda: matmul(
            self.value, other.value), context=self._context)

    def __or__(self, other):
        return F(self, other, function=lambda: or_(
            self.value, other.value), context=self._context)

    def __pow__(self, other):
        return F(self, other, function=lambda: pow(
            self.value, other.value), context=self._context)

    def __rshift__(self, other):
        return F(self, other, function=lambda: rshift(
            self.value, other.value), context=self._context)

    def __sub__(self, other):
        return F(self, other, function=lambda: sub(
            self.value, other.value), context=self._context)

    def __truediv__(self, other):
        return F(self, other, function=lambda: truediv(
            self.value, other.value), context=self._context)

    def __xor__(self, other):
        return F(self, other, function=lambda: xor(
            self.value, other.value), context=self._context)

    def __concat__(self, other):
        return F(self, other, function=lambda: concat(
            self.value, other.value), context=self._context)

    def __contains__(self, other):
        return F(self, other, function=lambda: contains(
            self.value, other.value), context=self._context)

    def __delitem__(self, other):
        return F(self, other, function=lambda: delitem(
            self.value, other.value), context=self._context)

    def __getitem__(self, other):
        return F(self, other, function=lambda: getitem(
            self.value, other.value), context=self._context)

    def __iadd__(self, other):
        return F(self, other, function=lambda: iadd(
            self.value, other.value), context=self._context)

    def __iand__(self, other):
        return F(self, other, function=lambda: iand(
            self.value, other.value), context=self._context)

    def __iconcat__(self, other):
        return F(self, other, function=lambda: iconcat(
            self.value, other.value), context=self._context)

    def __ifloordiv__(self, other):
        return F(self, other, function=lambda: ifloordiv(
            self.value, other.value), context=self._context)

    def __ilshift__(self, other):
        return F(self, other, function=lambda: ilshift(
            self.value, other.value), context=self._context)

    def __imod__(self, other):
        return F(self, other, function=lambda: imod(
            self.value, other.value), context=self._context)

    def __imul__(self, other):
        return F(self, other, function=lambda: imul(
            self.value, other.value), context=self._context)

    def __imatmul__(self, other):
        return F(self, other, function=lambda: imatmul(
            self.value, other.value), context=self._context)

    def __ior__(self, other):
        return F(self, other, function=lambda: ior(
            self.value, other.value), context=self._context)

    def __ipow__(self, other):
        return F(self, other, function=lambda: ipow(
            self.value, other.value), context=self._context)

    def __irshift__(self, other):
        return F(self, other, function=lambda: irshift(
            self.value, other.value), context=self._context)

    def __isub__(self, other):
        return F(self, other, function=lambda: isub(
            self.value, other.value), context=self._context)

    def __itruediv__(self, other):
        return F(self, other, function=lambda: itruediv(
            self.value, other.value), context=self._context)

    def __ixor__(self, other):
        return F(self, other, function=lambda: ixor(
            self.value, other.value), context=self._context)


class R(Value, Numeric):
    pass


def operations() -> dict:
    """produces all binary overloadable operations

    Returns:
        dict -- a dictionary of method_name -> binary_operation_name
    """
    return {k: v.__name__ for k, v in op.__dict__.items()
            if callable(v)
            and k.startswith('__')
            and len(signature(v).parameters) == 2
            and v.__name__ not in '__getitem__ __delitem__'}


def class_methods(clazz):
    methods = set(dir(clazz))
    unique_methods = methods.difference(
        *(dir(base()) for base in clazz.__bases__))
    return list(unique_methods)


def print_operations():
    """I am too lazy to type all the operator overriding methods. Here is
    how to use this helper:

    from jfaleiro_reactive.subject import operations
    print_operations()

    then paste both the import and the list of functions and adjust to remove the
    unary functions

    def __add__(self, other):
        return RFunctor(lambda: self.value + other.value,
                        context=self._context)
    """
    for k, v in operations().items():
        print(
            f"""def {k}(self, other):
                    return RFunctor(lambda: {v}(
                        self.value, other.value), context=self._context)
            """
        )
    imports = ', '.join(operations().values())
    print(f'from op import {imports}')
