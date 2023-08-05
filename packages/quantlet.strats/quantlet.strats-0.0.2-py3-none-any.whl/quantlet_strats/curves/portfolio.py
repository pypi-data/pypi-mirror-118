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

from quantlet_streaming.metadata import introspect_price
from quantlet_streaming.stream import QLet


@QLet
def cash_stock(
    iterable,
    size=10,
    initial_cash=500.0,
    load=2.0,
    price=None,
    buy="buy",
    sell="sell",
    porfolio_value="portfolio_value",
):
    """
    purchases a fixed sized lot based on initial cash balance
    """
    cash = initial_cash
    shares = stocks_value = 0.0
    for i in iterable:
        if price is None:
            price = introspect_price(i)
        p = i[price]
        value = p * size
        if buy in i:
            if cash >= (value + load):  # enough cash to buy?
                shares = shares + size
                cash = cash - value
                cash = cash - load
        if sell in i:
            if shares >= size:  # enough shares to sell?
                shares = shares - size
                cash = cash + value
                cash = cash - load
        stocks_value = shares * p
        portfolio_value = cash + stocks_value
        #        i['portfolio_value'] = portfolio_value
        #        i['cash_value'] = cash
        #        i['stocks_value'] = stocks_value
        i["alpha"] = portfolio_value / initial_cash
        yield i


@QLet
def gradual_execution(
    iterable,
    cash_balance,
    grading=1.0,
    load=2.0,
    price_column="price",
    buy_intention_column="buy_intention",
    sell_intention_column="sell_intention",
):
    shares_balance = 0
    last_buy_price = 0.0
    for i in iterable:
        price = i[price_column]
        if buy_intention_column in i:
            graded_cash_balance = cash_balance * grading
            shares = int(graded_cash_balance // price)
            if shares > 0:
                trade_value = shares * price
                cash_balance -= trade_value
                shares_balance += shares
                i["buy"] = price
                last_buy_price = price
        elif sell_intention_column in i:
            if shares_balance > 0 and price > last_buy_price:
                graded_shares_balance = max(1, int(shares_balance * grading))
                trade_value = graded_shares_balance * price
                cash_balance += trade_value
                shares_balance = shares_balance - graded_shares_balance
                i["sell"] = price
                last_buy_price = 0.0
        i["portfolio_value"] = shares_balance * price + cash_balance
        yield i


@QLet
def martingale_bet(
    iterable, cash_balance=1000, factor=2.0, initial_bet=10, reverse=False
):
    """
    manages a cash balance following a martingale bet, meaning either doubling
    a bet after a loss or after a win (reverse flag set)
    """
    current_bet = initial_bet
    bets = 0
    for i in iterable:
        i["bet"] = current_bet
        win = i["win"]
        if win:
            cash_balance += current_bet
            current_bet = current_bet * factor if reverse else initial_bet
        elif not win:
            cash_balance -= current_bet
            current_bet = initial_bet if reverse else current_bet * factor
        if cash_balance < 0:
            print("went broke on bet %s" % bets)
            break
        i["cash_balance"] = cash_balance
        bets += 1
        yield i


@QLet
def fixed_sized_delayed(iterator, size=10, cash=500.0, load=2, buy="buy",
                        sell="sell"):
    """
    purchases a fixed sized lot based on initial cash balance
    """
    initial_value = cash
    shares = 0
    signals = Queue()
    for i in iterator:
        # b = i[buy]
        s = i[sell]
        time_step, price, ma, signal = i
        value = None
        if signals.empty():
            s = ""
        else:
            s = signals.get()
            if s == "B":
                value = price * size
                if cash >= (value + load):  # enough cash to buy?
                    shares = shares + size
                    cash = cash - value - load
            elif s == "S":
                value = price * size
                if shares >= size:  # enough shares to sell?
                    shares = shares - size
                    cash = cash + value - load

        if signal == "B" or signal == "S":
            signals.put(signal)

        stocks = shares * price

        portfolio_value = cash + stocks
        yield time_step, price, ma, signal, cash, stocks, portfolio_value, (
            portfolio_value - initial_value
        ) / initial_value
