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

import pandas as pd

from ._version import __version__  # noqa: F401
from .alpaca import PAPER_REST_API, AlpacaProvider
from .common import (MAX_TIMESTAMP_UTC, MIN_ISO_TIME,  # noqa: F401
                     MIN_TIMESTAMP_UTC, STORE, IntervalEnum, SeriesTypeEnum,
                     TimeseriesProvider, epoch_to_timestamp)

_instance = TimeseriesProvider(AlpacaProvider(PAPER_REST_API), STORE)


def historic(ticker: str, series_type: str = 'ohlcv',
             interval: str = '1d', range_: tuple = None,
             adjusted: bool = False,
             instance: TimeseriesProvider = None) -> pd.DataFrame:
    """Generate historic financial time series

    Arguments:
        ticker {str} -- ticker symbol

    Keyword Arguments:
        series_type {str} -- type of the time-series (default: {'olhc'})
        interval {str} -- interval descriptor (e.g. 1m, 10s, 4h)
                          (default: {None})
        range {tuple} -- range tuple in the format (start, end)
                          (default: {None})

    Returns:
        [type] -- a dataframe with results
    """
    instance = _instance if instance is None else instance
    try:
        series_type_enum = SeriesTypeEnum[series_type.upper()]
    except KeyError:
        raise ValueError(
            f'invalid {series_type} '
            f'valid values are {[v.name for v in SeriesTypeEnum]}')
    return instance.historic(ticker=ticker,
                             series_type=series_type_enum,
                             interval=interval, adjusted=adjusted,
                             range_=range_)


def ts(begin, end, *args, **kwargs):
    for t in pd.date_range(begin, end, *args, **kwargs):
        yield collections.OrderedDict(x=t)
