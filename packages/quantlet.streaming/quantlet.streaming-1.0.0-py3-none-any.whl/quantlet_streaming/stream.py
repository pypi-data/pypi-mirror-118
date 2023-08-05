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

import functools
from concurrent.futures.thread import ThreadPoolExecutor

_DEFAULT_EXECUTOR = ThreadPoolExecutor()


class QLet(object):
    """
    decorator for QLet streams
    """

    def __init__(self, function, executor=None, expects=None):
        self._executor = _DEFAULT_EXECUTOR if executor is None else executor
        functools.update_wrapper(self, function)
        self.function = function

    def __call__(self, *args, **kwargs):
        return QLet(function=lambda ds: self.function(ds, *args, **kwargs))

    def __rrshift__(self, other):
        return self.function(other)

    def __ror__(self, other):
        return self._executor.submit(self.function, other)


def qlet(expects=None, provides=None):
    def wraps(f):
        return QLet(function=f, expects=expects)
    return wraps


@QLet
def as_type(ds, t):
    return t(ds)
