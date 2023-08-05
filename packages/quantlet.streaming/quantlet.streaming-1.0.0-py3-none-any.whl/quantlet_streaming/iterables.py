#
#     QuantLET-streaming - Elements of stream processing and data
#                          transformation in the QuantLET framework
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
import builtins
from types import GeneratorType

from .metadata import expects, register
from .stream import QLet

Canonical = GeneratorType


def container_to_canonical(container):
    for i in container:
        yield i


register(list, Canonical, container_to_canonical)
register(tuple, Canonical, container_to_canonical)


@QLet
@expects(Canonical)
def head(iterable, n=5):
    """ Retrieve n first items in iterable """
    for i in iterable:
        if n > 0:
            n -= 1
            yield i
        else:
            break


@QLet
@expects(Canonical)
def tail(iterable, n=5):
    return list(iterable)[-n:]


@QLet
@expects(Canonical)
def where(iterable, predicate):
    return (x for x in iterable if (predicate(x)))


@QLet
@expects(Canonical)
def tee(iterable, f):
    for i in iterable:
        f(i)
        yield i


@QLet
def select(iterable, *cols):
    for i in iterable:
        yield {k: i[k] for k in cols if k in i}


@QLet
def apply(iterable, f):
    return builtins.map(f, iterable)
