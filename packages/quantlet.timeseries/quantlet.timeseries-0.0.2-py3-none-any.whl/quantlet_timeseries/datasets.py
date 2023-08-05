#
#     QuantLET-timeseries - Fast timeseries functions and transformations
#                           in QuantLET
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
import collections
import os
import os.path as path

import numpy as np
import pandas as pd
import quandl
from quantlet_core.utils import mkdir_p, remove_files
from quantlet_streaming.stream import QLet

quantlet_dir = os.path.join(os.path.expanduser('~'), 'quantlet_datasets')

repository_dir = path.join(quantlet_dir, "repository")

KEY = os.environ.get("QUANDL_API_KEY", None)

quandl.ApiConfig.api_key = KEY


def purge_cache(symbol=None):
    # FIXME add deletion per symbol
    remove_files(repository_dir, "*.h5")


def index(symbol):
    cache_name = path.join(repository_dir, "%s_get.h5" %
                           symbol.replace("/", "_"))
    if not path.isfile(cache_name):
        mkdir_p(os.path.dirname(cache_name))
        if symbol == "sp500_current":
            df = pd.read_html(
                "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                header=0
            )[0]
            df.to_hdf(cache_name, symbol, format="table")
        else:
            raise "invalid symbol: " + symbol
    return pd.read_hdf(cache_name)


def historical(
    symbol,
    start=None,
    end=None,
    columns=None,
    collapse="daily",
    dict=True,
    reset_index=True,
):
    cache_name = path.join(
        repository_dir,
        "%s_%s" % (start, end),
        "%s_%s_get.h5" % (symbol.replace("/", "_"), collapse),
    )
    if not path.isfile(cache_name):
        mkdir_p(os.path.dirname(cache_name))
        if symbol.startswith("GOOG/"):
            d = quandl.get(symbol, collapse=collapse, authtoken=KEY)
        else:
            d = quandl.get("WIKI/" + symbol, collapse=collapse, authtoken=KEY)
        d.sort_index(inplace=True)
        d.to_hdf(cache_name, collapse, format="table")
    s = "index>=%s" % start.replace("-", "")
    e = "index<=%s" % end.replace("-", "")
    result = pd.read_hdf(cache_name, collapse, columns=columns, where=[s, e])
    if reset_index:
        result.reset_index(inplace=True)
    if dict:
        result = result.to_dict("records")
    return result


def retrieve(
    symbol,
    start=None,
    end=None,
    columns=None,
    collapse="daily",
    asdict=False,
    reset_index=False,
):
    return historical(symbol, start, end, columns, collapse, asdict,
                      reset_index)


@QLet
def apply(df, f=lambda x: x):
    return f(df)


@QLet
def to_canonical(df):
    return df.reset_index().to_dict("records")


to_dict = to_canonical


@QLet
def to_dataframe(iterable, index_column="index"):
    result = dict()
    for i in iterable:
        result[i[index_column]] = i
    df = pd.DataFrame.from_dict(result, orient="index")
    return df.drop(columns=[index_column])


from_dict = to_dataframe


@QLet
def set_column(df, col, f=lambda x: x):
    df[col] = f(df)
    return df


@QLet
def dataframe(iterable, index="x"):
    df = pd.DataFrame(list(iterable))
    if index is not None:
        return df.set_index([index])  # FIXME x must be introspected
    else:
        return df


def forward_rolling(df: pd.DataFrame, column: str,
                    freq: str, func) -> np.ndarray:
    """
    generates a forward-rolling of the column, applying func to the rolling
    window

    Arguments:
        df {pd.DataFrame} -- dataframe holding the data
        column {str} -- column where the rolling will take place
        freq {str} -- the frequency description ('1s', '2min', etc)
        func {[type]} -- the function to apply the rolling window

    Returns:
        np.ndarray -- the array of values for each of window starting indexes
    """
    delta = pd.to_timedelta(freq)
    result = np.zeros(len(df.index))
    for i, (index, _) in enumerate(df[column].items()):
        mask = (df.index >= index) & (df.index < (index + delta))
        window = df[mask][column]
        # window = df.loc[index:index + delta][column]
        result[i] = func(window.values)
    return result


def reverse_rolling(df: pd.DataFrame, column: str,
                    freq: str, func) -> np.ndarray:
    """
    generates a rolling on reverse of the original index ordering

    Arguments:
        df {pd.DataFrame} -- [dataframe]
        column {str} -- [column to roll]
        freq {str} -- [the frequency description ('1s', '2min', etc)]
        func {[type]} -- [the function to apply to the rolling windown]

    Returns:
        np.ndarray -- [a reversed rolled sequence]
    """
    delta = pd.to_timedelta(freq)
    window = collections.deque()
    result = np.zeros((len(df.index)))
    for i, (index, data) in enumerate(df[::-1].iterrows()):
        window.appendleft((index, data[column]))
        while len(window) > 0 and index > (window[-1][0] + delta):
            window.pop()
        result[i] = func([w[1] for w in window])
    return result[::-1]
