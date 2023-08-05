#
#     QuantLET-strats - QuantLET strategies, statistics, curves, filters,
#                       and financial engineering functions.
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
from collections import deque

import pandas as pd
from quantlet_streaming.iterables import Canonical
from quantlet_streaming.metadata import expects
from quantlet_streaming.stream import QLet


@QLet
@expects(pd.DataFrame)
def bollinger(df, ma_tag='ma', std_tag='std',
              upper_tag='upper', lower_tag='lower',
              window=20, stds=2.0):
    """Bollinger band. A band around a moving average that becomes narrower as
    volatility decreases

    Arguments:
        df {[type]} -- [a dataframe]

    Keyword Arguments:
        ma_tag {str} -- [column name for the moving average] (default: {'ma'})
        std_tag {str} -- [column name for the standard deviation] (default:
                          {'std'})
        upper_tag {str} -- [column name for the upper band] (default:
                          {'upper'})
        lower_tag {str} -- [column name for the lower band] (default:
                          {'lower'})
        window {int} -- [size of the window over which to calculate the
                         standard deviation] (default: {20})
        stds {float} -- [number of standard deviations] (default: {2.0})

    Returns:
        [type] -- [description]
    """
    df[upper_tag] = df[ma_tag] + (df[std_tag] * stds)
    df[lower_tag] = df[ma_tag] - (df[std_tag] * stds)
    return df


@QLet
@expects(pd.DataFrame)
def fixed(df, ma_tag='ma', upper_tag='upper', lower_tag='lower',
          window=20, ratio=.25):
    df[upper_tag] = df[ma_tag] + (df[ma_tag] * ratio)
    df[lower_tag] = df[ma_tag] - (df[ma_tag] * ratio)
    return df


@QLet
@expects(Canonical)
def rolling(iterable, function, window_size, out_column=None,
            in_column="price"):
    """
    rolling measurements
    """
    out_column = ("rolling_%s" % function.__name__
                  if out_column is None else out_column)
    window = deque([], window_size)
    for i in iterable:
        window.appendleft(i[in_column])
        i[out_column] = function(window)
        yield i


@QLet
@expects(Canonical)
def high_low(iterable, price_column="price"):
    for i in iterable:
        higher, lower, price = (i["rolling_max"],
                                i["rolling_min"],
                                i[price_column])
        if lower < higher:
            if price >= higher:
                i["sell_intention"] = price
            elif price <= lower:
                i["buy_intention"] = price
        yield i
