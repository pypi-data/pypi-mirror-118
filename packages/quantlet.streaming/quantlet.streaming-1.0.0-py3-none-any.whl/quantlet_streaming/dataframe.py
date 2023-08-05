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
import pandas as pd
from quantlet_core.utils import is_function

from .iterables import Canonical
from .metadata import expects, register
from .stream import QLet


def is_dataframe(item):  # TODO candidate to quantlet_core
    return isinstance(item, pd.DataFrame)


def dataframe_to_list(df):
    return df.reset_index().to_dict(orient="records")


def canonical_to_dataframe(item, index_column='index'):
    items = dict()
    for i in item:
        items[i[index_column]] = i
    result_df = pd.DataFrame.from_dict(items, orient="index")
    return result_df.drop(columns=[index_column])


register(pd.DataFrame, list, dataframe_to_list)
register(Canonical, pd.DataFrame, canonical_to_dataframe)


@QLet
@expects(pd.DataFrame)
def head(df, n=5):
    """ Retrieve n first items in dataset """
    return df.head(n)


@QLet
@expects(pd.DataFrame)
def tail(df, n=5):
    return df.tail(n)


@QLet
@expects(pd.DataFrame)
def select(df, *args, **kwargs):
    if args != tuple():
        if all(isinstance(i, str) for i in args):
            return df[list(args)]
        elif len(args) == 1:
            p = args[0]
            if is_function(p):
                return df.rename(mapper=p, axis=1)
            elif isinstance(p, list):
                return df >> select(*p)
            elif isinstance(p, dict):
                return df >> select(**p)
            else:
                raise ValueError(f'invalid arguments: {p}')
        else:
            raise ValueError(f'invalid arguments: {args}')
    if kwargs != dict():
        return df.rename(columns=kwargs)
    return df
