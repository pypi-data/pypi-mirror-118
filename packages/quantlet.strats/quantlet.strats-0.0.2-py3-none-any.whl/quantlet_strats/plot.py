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

import queue
import threading

# import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import lag_plot as pandas_lag_plot
from pandas.plotting import scatter_matrix as pandas_scatter_matrix
from quantlet_streaming.metadata import expects
from quantlet_streaming.stream import QLet


def show():
    plt.show()


@QLet
def animate(iterable, exclude=dict(), ylim=(-2.0, 2.0), xlim=(0, 3.0)):
    """
    plot animation
    """

    fig, ax = plt.subplots()
    (_,) = ax.plot([], [], lw=1)
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlim(xlim[0], xlim[1])

    lines = {}
    lines_array = []
    data_array = {}

    def update(data):
        if data:  # None is end of stream
            xdata = update.xdata
            xmax = update.xmax
            xdata.append(update.i)
            xdata = xdata[-xmax:]  # truncate

            for k in data.keys():
                if k not in exclude:
                    if k not in lines:
                        (l,) = ax.plot([], [], lw=1, label=k)
                        lines[k] = l
                        lines_array.append(l)
                        data_array[k] = []
                    ydata = data_array[k]
                    ls = lines[k]
                    ydata.append(data[k])
                    ydata = ydata[-xmax:]  # truncate
                    ls.set_data(xdata, ydata)
                    ls.set_label(k)

            if xdata[0] != xdata[-1]:
                ax.set_xlim(xdata[0], xdata[-1])
            update.i += 1
        return lines_array

    update.xdata = []
    update.i = 0
    update.xmax = 30

    q = queue.Queue(maxsize=100)

    def data_gen():
        yield q.get(block=True)

    def worker():
        # time.sleep(3) # hack - animation takes forever to clear
        for i in iterable:
            q.put(i, block=True)
        q.put(None)

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

    def init():
        return lines_array

    ax.legend(loc=2)

    # ani = animation.FuncAnimation(
    #     fig, update, data_gen, init_func=init, blit=True, interval=100
    # )

    plt.show()


@QLet
def lag_plot(iterable, index="x"):
    df = pd.DataFrame(list(iterable))
    if index is not None:
        df.set_index([index], inplace=True)
    pandas_lag_plot(df)


@QLet
@expects(pd.DataFrame)
def plot_error(
    df,
    index_column="index",
    figsize=(12, 12),
    price_tag="price",
    price_prediction_tag="price_prediction",
    error_tag="error",
    ewme_tag="ewme",
    primary_logy=True,
):
    p = df.copy()
    p[price_tag].plot(
        alpha=0.8, figsize=figsize, secondary_y=True, legend=True, grid=True
    )
    p[price_prediction_tag].plot(alpha=0.8, secondary_y=True, legend=True)
    p[error_tag].plot(alpha=0.3, logy=primary_logy, legend=True)
    p[ewme_tag].plot(alpha=0.5, logy=primary_logy, legend=True)
    return df


@QLet
@expects(pd.DataFrame)
def plot(df, out=None, index="x", columns=None, alpha=0.5):
    print(df.columns)
    if index in df.columns:
        df.set_index([index], inplace=True)
    if columns is not None:
        df = df[columns]  # circumventing a bug on pandas column ordering

    def style_of(c):
        cu = c.lower()
        if cu == "buy":
            return "^g"  # '^' # ^g'
        elif cu == "sell":
            return "vr"  # 'v' #'vr'
        else:
            return None

    styles = [style_of(c) for c in df.columns]

    def secondary_y_of(c):
        cl = c.lower()
        return cl.endswith("value") or cl.endswith("alpha")

    secondary_y = [c for c in df.columns if secondary_y_of(c)]
    df.plot(alpha=alpha, style=styles, secondary_y=secondary_y)


@QLet
@expects(pd.DataFrame)
def scatter_matrix(df, index="x", fast=False, **scatter_kwargs):
    if index is not None:
        df.set_index([index], inplace=True)
    if fast:
        pandas_scatter_matrix(df, **scatter_kwargs)
    else:
        sns.set(style="white")
        g = sns.PairGrid(df, diag_sharey=False)
        g.map_lower(sns.kdeplot, cmap="Blues_d")
        #   g.map_upper(plt.scatter)
        #        g.map_upper(sns.lmplot)
        g.map_upper(sns.regplot)
        g.map_diag(sns.kdeplot, lw=3)


@QLet
@expects(pd.DataFrame)
def hist(df, feature="fitness", rug=False):
    sns.distplot(df, rug=rug)
