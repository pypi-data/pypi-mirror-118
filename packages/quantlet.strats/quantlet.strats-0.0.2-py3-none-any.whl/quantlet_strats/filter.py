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

import pandas as pd
from quantlet_streaming.iterables import Canonical
from quantlet_streaming.metadata import expects, introspect_price
from quantlet_streaming.stream import QLet


@QLet
def cma(iterables, input=None, output="cma", recursive=False):
    """
    cumulative moving average
    :param iterables: stream generator
    :param input: input tag meta-data
    :param output: output tag meta-data
    :param recursive: recursive mode
    """
    cma_ = count = 0.0
    if recursive:
        for i in iterables:
            if input is None:
                input = introspect_price(i)
            value = i[input]
            try:
                cma_ = (value + (count - 1) * cma_) / count
            except BaseException:
                cma_ = value
            i[output] = cma
            yield i
    else:
        total = 0.0
        for i in iterables:
            if input is None:
                input = introspect_price(i)
            value = i[input]
            total = total + value
            count = count + 1
            i[output] = total / count
            yield i


ma = cma  # backwards compatible


@QLet
def rma(iterables, m=100, input=None, output="rma", recursive=True):
    """
    rolling moving average over window of size m
    :param iterables: stream generator
    :param m: rolling window size
    :param input: input tag meta-data
    :param output: output tag meta-data
    :param recursive: recursive mode
    """
    window = []
    rma_ = None
    if recursive:
        for i in iterables:
            if input is None:
                input = introspect_price(i)
            value = i[input]
            window.append(value)
            len_window = float(len(window))
            if rma_ is None:
                rma_ = value
            elif len_window > m:
                tail = window.pop(0)
                rma_ = rma_ + (value - tail) / m  # recursive rma
            else:
                # window creation ongoing, uses non-recursive cma
                rma_ = (
                    value + (len_window - 1) * rma_
                ) / len_window
            i[output] = rma_
            yield i
    else:
        for i in iterables:
            if input is None:
                input = introspect_price(i)
            value = i[input]
            window.append(value)
            rma = sum(window) / float(len(window))
            i[output] = rma
            yield i


@QLet
@expects(Canonical)
def ewma(iterables, input_tag, output_tag="ewma", alpha=0.1, recursive=True):
    """
    exponentially moving average with decaying factor alpha
    :param iterables: stream generator
    :param alpha: decaying factor
    :param input_tag: input tag meta-data
    :param output_tag: output tag meta-data
    :param recursive: recursive mode
    """
    one_minus_alpha = 1.0 - alpha
    ewma_ = None
    if recursive:
        for i in iterables:
            value = i[input_tag]
            if ewma_ is None:
                ewma_ = value
            else:
                ewma_ = (
                    value * alpha +
                    one_minus_alpha * ewma_
                )  # recursive form EWMA
            i[output_tag] = ewma_
            yield i
    else:
        raise "not supported"


@QLet
@expects(pd.DataFrame)
def std(df, price_tag='p', std_tag='std', window=20):
    df[std_tag] = df[price_tag].rolling(window=window).std()
    return df
