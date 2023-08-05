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
import os

import alpaca_trade_api as api
import pandas as pd
import yaml
from alpaca_trade_api.entity import BarSet

from .common import BASES, AbstractProvider, IntervalEnum, SeriesTypeEnum

BASE_URL = dict(paper="https://paper-api.alpaca.markets",
                production="https://api.alpaca.markets")

logger = logging.getLogger(__name__)


def read_bars(file_name: str) -> BarSet:
    """Generate a BaseSet from a text description of dictionaries and lists

    Arguments:
        file_name {str} -- File name

    Returns:
        BarSet -- A populated BarSet object
    """
    from alpaca_trade_api.entity import Bar, Bars, BarSet  # noqa: F401
    with open(file_name, 'r') as f:
        lines = ''.join(f.readlines())
    return BarSet(eval(lines))


def raw_to_barset(raw: dict) -> BarSet:
    return BarSet(dict)


def barset_to_raw(barset: BarSet) -> dict:
    return barset._raw


ALPACA_ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def iso8601_alpaca_to_epoch(iso_date: str) -> int:
    """Convert a alpaca-speific ISO8601 to an epoch long

    Arguments:
        iso_date {str} -- Alpaca formatted ISO8601 string
                          (e.g. '2019-01-01T00:00:00Z')

    Returns:
        int -- number of seconds since epoch
    """
    '%Y-%m-%dT%H:%M:%SZ'
    return calendar.timegm(
        datetime.datetime.strptime(
            iso_date,
            ALPACA_ISO8601_FORMAT).timetuple()
    )


def iso8601_alpaca_to_timestamp(iso: str) -> pd.Timestamp:
    return pd.Timestamp(iso, tz='UTC')


def timestamp_to_alpaca_iso8601(ts: pd.Timestamp) -> str:
    return ts.strftime(ALPACA_ISO8601_FORMAT)


class Rest(object):

    def __init__(self, base: str = 'paper', version: str = 'v2',
                 config: str = '~/.config/quantlet/keys',
                 file_name: str = 'alpaca.yaml'):
        try:
            assert base in BASES, '%s not in %s' % (base, BASES)
            assert base in BASE_URL.keys(
            ), f'{base} does not have an URL in {BASE_URL}'
            with open(os.path.expanduser(
                    os.path.join(config, file_name)), 'r') as f:
                keys = yaml.load(f, Loader=yaml.FullLoader)[base]
            self._rest = api.REST(key_id=keys['id'], secret_key=keys['secret'],
                                  api_version=version, base_url=BASE_URL[base])
            self._exception = None
        except Exception as e:
            logger.exception('exception caught on rest API init')
            self._exception = e

    @property
    def api(self) -> api.REST:
        if self._exception is None:
            return self._rest
        else:
            raise self._exception


PAPER_REST_API = Rest(base='paper')
PRODUCTION_REST_API = Rest(base='production')

MAX_ALPACA_GET_BARS: int = 1000


class AlpacaProvider(AbstractProvider):
    """
    Provider of Alpaca timeseries data.
    documentation:
    https://pypi.org/project/alpaca-trade-api/
    """

    _to_timeframe = {IntervalEnum.DAILY: 'day',
                     IntervalEnum.MINUTE: 'minute'}
    _to_interval_size = {IntervalEnum.DAILY: set([1]),
                         IntervalEnum.MINUTE: set([1, 5, 15])}

    def __init__(self, rest: Rest, limit: int = MAX_ALPACA_GET_BARS):
        self._rest = rest
        self._limit = limit

    @property
    def source(self) -> str:
        return 'alpaca'

    def _get_bars2(self, ticker: str, timeframe: str, start: pd.Timestamp,
                   end: pd.Timestamp) -> pd.DataFrame:
        last_retrieved_date = start
        result = pd.DataFrame()
        while True:
            barset = self._rest.api.get_barset(
                ticker, timeframe,
                start=timestamp_to_alpaca_iso8601(start),
                end=timestamp_to_alpaca_iso8601(end)
            )
            bars = barset[ticker].df
            if bars.empty or last_retrieved_date == bars.index[-1]:
                return result
            last_retrieved_date = bars.index[-1]
            result = pd.concat([result, bars])

    def _get_bars(self, ticker: str, timeframe: str, start: pd.Timestamp,
                  end: pd.Timestamp) -> pd.DataFrame:
        barset = self._rest.api.get_barset(ticker, timeframe,
                                           start=timestamp_to_alpaca_iso8601(
                                               start),
                                           end=timestamp_to_alpaca_iso8601(
                                               end),
                                           limit=self._limit,
                                           )
        bars = barset[ticker].df
        if bars.empty:
            return bars
        last_retrieved_date = bars.index[-1]
        logger.info(f'{timeframe}:{ticker}:{start}:{end} ->'
                    f'{last_retrieved_date} count={len(bars.index)}')
        if last_retrieved_date < end:
            return pd.concat([bars,
                              self._get_bars(ticker, timeframe,
                                             last_retrieved_date, end)])
        else:
            return bars

    def historic(self,
                 ticker: str,
                 series_type: SeriesTypeEnum,
                 interval: IntervalEnum,
                 interval_size: int,
                 adjusted: bool,
                 start: pd.Timestamp,
                 end: pd.Timestamp):
        assert series_type == SeriesTypeEnum.OHLCV, (
            f'invalid series_type {series_type}, {type(series_type)}, '
            f'{series_type == SeriesTypeEnum.OHLCV}, '
            f'{series_type is SeriesTypeEnum.OHLCV}')
        assert interval in self._to_timeframe, (
            f'interval {interval} not supported, '
            f'valid={self._to_timeframe.keys()}')
        assert interval_size in self._to_interval_size[
            interval], (f'invalid interval_size: {interval_size} '
                        f'allowed interval sizes for {interval} '
                        f'are {self._to_interval_size[interval]}')
        assert not adjusted, 'adjusted prices flag not supported'
        timeframe = self._to_timeframe[interval]
        return self._get_bars2(ticker, timeframe,
                               start=start, end=end)


class AlpacaAlphaVantageProvider(AbstractProvider):
    """
    Provider of Alpha Vantage timeseries data.
    The Alpha Vantage endpoint documentation:
    https://www.alphavantage.co/documentation/#
    """

    _allowed_series_type = set([SeriesTypeEnum.OHLC, SeriesTypeEnum.OHLCV])

    _to_cadence = {
        IntervalEnum.DAILY: 'daily',
        IntervalEnum.WEEKLY: 'weekly',
        IntervalEnum.MONTHY: 'monthly',
    }

    def __init__(self, rest):
        self.rest = rest

    def source(self) -> str:
        return 'alpaca-alphavantage'

    def historic(self, ticker: str,
                 series_type: SeriesTypeEnum,
                 interval: IntervalEnum,
                 interval_size: int,
                 adjusted: bool,
                 start: pd.Timestamp,
                 end: pd.Timestamp):
        assert series_type in AlpacaAlphaVantageProvider._allowed_series_type
        assert interval in AlpacaAlphaVantageProvider._to_cadence.keys()
        assert interval_size == 1
        cadence = AlpacaAlphaVantageProvider._to_cadence[interval]
        result = self.rest.api.alpha_vantage.historic_quotes(
            ticker,
            adjusted=adjusted,
            outputsize='compact',
            cadence=cadence,
            output_format='pandas')
        mapping = {v: v[3:].replace(' ', '_') for v in result.columns}
        return result.rename(columns=mapping)
