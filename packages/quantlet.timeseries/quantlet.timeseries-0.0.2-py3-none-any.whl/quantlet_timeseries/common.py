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
import calendar
import datetime
import logging
import re
from abc import ABC, abstractmethod
from enum import Enum, unique

import pandas as pd
from jfaleiro_tsstore import AbstractRoot, root

BASES = 'paper production'.split()

_logger = logging.getLogger(__name__)


@unique
class IntervalEnum(Enum):
    SECOND = 's'
    MINUTE = 'm'
    HOUR = 'h'
    DAILY = 'd'
    WEEKLY = 'w'
    MONTHY = 'M'


IntervalEnum.reverse = {c.value: c for c in IntervalEnum}


@unique
class SeriesTypeEnum(Enum):
    OHLC = 0  # open high low close
    OHLCV = 1  # OHLC + volume
    OHLCVDS = 2  # OHLCV + dividend + split


class AbstractProvider(ABC):

    @property
    @abstractmethod
    def source(self) -> str:
        pass

    @abstractmethod
    def historic(self,
                 ticker: str,
                 series_type: SeriesTypeEnum,
                 interval: IntervalEnum,
                 interval_size: int,
                 adjusted: bool,
                 start: pd.Timestamp,
                 end: pd.Timestamp):
        pass


STORE = root('~/quantlet-ts', type_='fastparquet')

MIN_ISO_TIME = '1677-09-23T00:00:00Z'
MAX_ISO_TIME = '2262-01-01T00:00:00Z'

# MIN_TIMESTAMP_UTC = pd.Timestamp.min.tz_localize('UTC')
MIN_TIMESTAMP_UTC = pd.Timestamp(MIN_ISO_TIME)
# MAX_TIMESTAMP_UTC = pd.Timestamp.max.tz_localize('UTC')
MAX_TIMESTAMP_UTC = pd.Timestamp(MAX_ISO_TIME)


def epoch_to_timestamp(epoch: int, tz='UTC') -> pd.Timestamp:
    return pd.Timestamp(epoch, unit='s', tz=tz)


def iso8601_to_epoch(iso_date: str) -> int:
    """Convert a ISO-8601 to an epoch long

    Arguments:
        iso_date {str} -- ISO-8601 string (e.g. '1984-06-02T19:05:00.000Z')

    Returns:
        int -- number of seconds since epoch
    """
    '%Y-%m-%dT%H:%M:%SZ'
    return calendar.timegm(
        datetime.datetime.strptime(iso_date,
                                   "%Y-%m-%dT%H:%M:%S.%f").timetuple()
    )


PATTERN = re.compile(r'([\d]+)([a-zA-Z])')


def _fix_naive_tz(ds):
    """ fastparquet bug hack - TODO move to jfaleiro.tsstore
    https://github.com/dask/fastparquet/issues/433
    """
    if any(x.tzinfo is None for x in ds.index):
        import pytz
        _logger.warning('index is naive, cant have that, coercing for UTC')
        ds.index = [x.replace(tzinfo=pytz.utc) for x in ds.index]
    return(ds)


class TimeseriesProvider(object):

    def __init__(self, provider: AbstractProvider,
                 store: AbstractRoot) -> None:
        self.provider = provider
        self.root = store

    @staticmethod
    def _range_defaults(range):
        def _default(value, default):
            value = default if value is None else value
            value = pd.to_datetime(value,
                                   utc=True) if isinstance(
                                       value,
                                       str) else value
            return value
        range = (None, None) if range is None else range
        range = (_default(range[0], MIN_TIMESTAMP_UTC),
                 _default(range[1], MAX_TIMESTAMP_UTC))
        return range

    @staticmethod
    def _collection_name(series_type: IntervalEnum,
                         interval: IntervalEnum, interval_size: int):
        return str((series_type.name, interval.name, interval_size))

    @staticmethod
    def _split_duration(time_val: str) -> tuple:
        groups = PATTERN.match(time_val).groups()
        if len(groups) != 2:
            raise ValueError(
                'cannot parse %s into a quantity and unit' % time_val)
        quantity, unit = groups
        quantity, unit = int(quantity), unit.lower()
        if unit not in IntervalEnum.reverse.keys():
            raise ValueError('invalid unit %s, possible values are %s' %
                             (unit, IntervalEnum.reverse.keys()))
        return quantity, IntervalEnum.reverse[unit]

    def historic(self, ticker: str, series_type: SeriesTypeEnum,
                 interval: str, adjusted: bool = True, range_: tuple = None):
        range_ = self._range_defaults(range_)
        assert range_[0] <= range_[
            1], f'{range_}: range[0] must be <= range[1]'
        interval_size, interval = self._split_duration(interval)
        collection = self.root.get_store(series_type=series_type.name,
                                         interval=interval.name,
                                         interval_size=interval_size,
                                         adjusted=adjusted,
                                         )
        series = collection.get(ticker)
        if series is None:
            series = self.provider.historic(ticker=ticker,
                                            series_type=series_type,
                                            interval=interval,
                                            interval_size=interval_size,
                                            adjusted=adjusted,
                                            start=range_[0],
                                            end=range_[1])
            collection.put(ticker, series)
        else:
            series = _fix_naive_tz(series)
            first, last = series.index[0], series.index[-1]
            print(range_, first, last)
            if range_[0] < first:
                range_slice = range_[0], first
                head_slice = self.provider.historic(
                    ticker=ticker,
                    series_type=series_type,
                    interval=interval,
                    interval_size=interval_size,
                    adjusted=adjusted,
                    start=range_slice[0],
                    end=range_slice[1])
                if not head_slice.empty:
                    collection.prepend(ticker, head_slice)
            if range_[1] > last:
                range_slice = last, range_[1]
                tail_slice = self.provider.historic(
                    ticker=ticker,
                    series_type=series_type,
                    interval=interval,
                    interval_size=interval_size,
                    adjusted=adjusted,
                    start=range_slice[0],
                    end=range_slice[1])
                collection.append(ticker, tail_slice)

        result = collection.get(ticker)
        result.index.name = None
        # return result.loc[range_[0]:range_[1]]
        return result[(
            result.index >= range_[0]) & (result.index <= range_[1])]
