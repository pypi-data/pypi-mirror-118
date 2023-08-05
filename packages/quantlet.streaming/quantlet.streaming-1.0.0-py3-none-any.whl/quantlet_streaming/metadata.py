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
from functools import wraps

import networkx as nx


class NoTransformationPath(Exception):
    pass


class CyclicalTransformationPath(Exception):
    pass


class NoTransformationForType(Exception):
    pass


class Registry(object):
    def __init__(self, graph=None):
        self.graph = nx.DiGraph() if graph is None else graph

    def register(self, from_, to_, function):
        self.graph.add_edge(from_, to_, function=function)

    def deregister(self, from_, to_):
        try:
            return self.graph.get_edge_data(from_, to_)['function']
        finally:
            self.graph.remove_edge(from_, to_)

    def transformer(self, from_, to_):
        def transform(item):
            try:
                if not nx.has_path(self.graph, from_, to_):
                    raise NoTransformationPath(from_, to_)
            except nx.NodeNotFound:
                raise NoTransformationForType(from_, to_)
            nodes = nx.shortest_path(self.graph, source=from_, target=to_)
            for i in range(len(nodes) - 1):
                f = self.graph.get_edge_data(
                    nodes[i], nodes[i + 1])['function']
                item = f(item)
            return item
        return transform


_registry = Registry()

register = _registry.register
deregister = _registry.deregister
transformer = _registry.transformer


def expects(type_, t=None, **kwparams):
    def decorator(f):
        @wraps(f)
        def wrapper(container, *args, **kwargs):
            if isinstance(container, type_):
                def t(x): return x
            else:
                t = transformer(type(container), type_)
            return f(t(container, **kwparams), *args, **kwargs)
        return wrapper
    return decorator


def introspect_price(d):
    for c in ["brownian", "price", "y"]:
        if c in d:
            return c


def introspect_ma(d):
    for k in d:
        if k.endswith("ma"):
            return k


LINE = """
**** PROVENANCE hdf://quantlet/jfaleiro/goog_momentum.png ****

quandl.get('https://www.quandl.com/data/WIKI/GOOG')
`-- v N/A jfaleiro @ 8/15/2015 14:35:12 EST

historical.cache('hdf://quantlet/pub/quandl/WIKI/GOOG.h5')
`-- v 0.0.1 jfaleiro @ 8/15/2015 14:35:12 EST MD5:d9d914b9bdcd9fccd913d4ab7790

stream
    quantlet_analytics.dataset
    historical('GOOG', '2014-01-01', '2014-12-31', columns=['Adj. Close'])
    `--- v 0.0.1 jfaleiro @ 1/1/2015 8:34:02 EST MD5:29bc31efd050df78976a2b852
    quantlet.filter
    ewma
    `--- v 0.0.1 jfaleiro @ 1/1/2015 8:34:02 EST MD5:9ed435ab2b00f1afdf4ff79cc
    quantlet.strats.momentum
    maco
    `--- v 0.0.1 jfaleiro @ 1/1/2015 8:34:02 EST MD5:9ed435ab2b00f1afdf4ff79cc
    quantlet.strats.portfolio
    cash_stock(initial_cash=10000, load=7.5)
    `--- v 0.0.1 jfaleiro @ 1/1/2015 8:34:02 EST MD5:9ed435ab2b00f1afdf4ff79cc
    quantlet_analytics.plot
    plot(out='goog_momentum.png')
    `--- v 0.0.1 jfaleiro @ 9/1/2015 8:15:35 EST MD5:ecfc5d3f498074e79cbb0b309

file('hdf://quantlet/jfaleiro/goog_momentum.png')
`-- v N/A jfaleiro @ 9/17/2015 21:05:02 EST MD5:72802afc4283d8077da1cb368aa6c2

**** end of hdf://quantlet/jfaleiro/goog_momentum.png ****
        """


def provenance(url):  # pragma: no cover
    if url == "goog_momentum.png":
        print(LINE)
