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

from queue import Queue

from quantlet_streaming.metadata import introspect_ma, introspect_price
from quantlet_streaming.stream import QLet


@QLet
def maco_direct(iterator, size=10, cash=500.0, load=2.0):
    """
    moving_average_cross_over

    If the spot price:
     crosses the MA upward is considered as a BUY signal.
     crosses the MA downward is considered as a SELL signal.
    """
    initial_value = cash
    last_price = last_ma = None
    shares = 0
    for i in iterator:
        time_step, price, ma = i
        if not last_price:
            last_price = price
        value = None
        signal = ""
        if last_ma > last_price and price > ma > last_price:  # buy
            signal = "B"
        if last_ma < last_price and price < ma < last_price:  # sell
            if shares > 0:
                signal = "S"

        if signal == "B":
            value = price * size
            shares = shares + size
            cash = cash - value - load
        elif signal == "S":
            value = price * size
            shares = shares - size
            cash = cash + value - load
        stocks = shares * price

        last_ma = ma
        last_price = price
        portfolio_value = cash + stocks
        yield time_step, price, ma, signal, cash, stocks, portfolio_value, (
            portfolio_value - initial_value
        ) / initial_value


@QLet
def maco2(iterator, size=10, cash=500.0, load=2.0):
    """
    moving_average_cross_over

    If the spot price:
     crosses the MA upward is considered as a BUY signal.
     crosses the MA downward is considered as a SELL signal.
    """
    initial_value = cash
    last_price = last_ma = None
    shares = 0
    signals = Queue()
    for i in iterator:
        time_step, price, ma = i
        if not last_price:
            last_price = price
        value = None
        if not signals.empty():
            signal = signals.get()
            if signal == "B":
                value = price * size
                shares = shares + size
                cash = cash - value - load
            elif signal == "S":
                value = price * size
                shares = shares - size
                cash = cash + value - load

        signal = ""
        if last_ma > last_price and price > ma > last_price:  # buy
            signal = "B"
            signals.put(signal)
        if last_ma < last_price and price < ma < last_price:  # sell
            if shares > 0:
                signal = "S"
                signals.put(signal)

        stocks = shares * price

        last_ma = ma
        last_price = price
        portfolio_value = cash + stocks
        yield time_step, price, ma, signal, cash, stocks, portfolio_value, (
            portfolio_value - initial_value
        ) / initial_value


@QLet
def maco(iterator, spot=None, ma=None, buy="buy", sell="sell"):
    """
    cross-over momentum strategy

    If the spot price:
     crosses the MA upward is considered as a BUY signal.
     crosses the MA downward is considered as a SELL signal.
    """
    # BUY = "B"
    # SELL = "S"
    last_price = last_ma = None
    for i in iterator:
        if spot is None:
            spot = introspect_price(i)
        if ma is None:
            ma = introspect_ma(i)
        price = i[spot]
        m = i[ma]
        if last_price is None:
            last_price = price
        if last_ma is None:
            last_ma = ma
        if last_ma > last_price and price > m > last_price:  # buy
            i[buy] = price
        if last_ma < last_price and price < m < last_price:  # sell
            i[sell] = price

        last_price = price
        last_ma = m
        yield i
