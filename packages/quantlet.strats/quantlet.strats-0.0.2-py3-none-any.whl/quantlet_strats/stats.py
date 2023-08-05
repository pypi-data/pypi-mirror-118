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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from quantlet_streaming.stream import QLet


def unif(a, b, n):
    """
    Uniform distribution
    """
    return (b - a) * np.random.sample(n) + a


def autocorrelation(series):
    """
    Calculate autocorrelation instances exactly like autocorrelation_plot does
    """
    from statsmodels.compat.python import lmap
    n = len(series)
    data = np.asarray(series)
    mean = np.mean(data)
    c0 = np.sum((data - mean) ** 2) / float(n)

    def r(h):
        return ((data[: n - h] - mean) * (data[h:] -
                                          mean)).sum() / float(n) / c0

    return np.array(lmap(r, np.arange(n) + 1))


def inflection_points(y, dx=0.01, gaussian=3.0):
    """
    find inflection points, gaussian-filters first
    """
    from scipy.ndimage import gaussian_filter

    return np.diff(gaussian_filter(y, gaussian)) / dx


@QLet
def plot_autocorrelation(
    serie,
    figsize=(12, 8),
    ax=plt,
    threshold=0.005,
    type="long",
    maxlags=30,
    title="",
    print_inflections=False,
    plot_inflections=True,
    decompose_freq=365,
    window=90,
):
    """
    plot autocorrelation in either long (recommended) or short lags.
    """
    if ax == plt:
        plt.figure(figsize=figsize)
    xs = serie.replace([np.inf, -np.inf, 0], np.nan).dropna()
    if type == "long":
        from pandas.plotting import autocorrelation_plot

        if ax != plt:
            ax.set_title(title)
            autocorrelation_plot(xs, ax=ax)
        else:
            autocorrelation_plot(xs)
        acs = autocorrelation(xs)
        gradients = inflection_points(acs)
        idx = np.nonzero(
            np.logical_and(gradients < +threshold, gradients > -threshold)
        )[0]
        if plot_inflections:
            plt.plot(idx, acs[idx], "r*")
        if print_inflections:
            print("approx inflections @ (x,y)=", list(
                zip(idx, np.round(acs[idx], 2))))
    elif type == "short":
        plt.xlabel("lag")
        plt.ylabel("correlation")
        if ax == plt:
            plt.acorr(xs, maxlags=maxlags)
        else:
            plt.acorr(xs, maxlags=maxlags, ax=ax)
    elif type == "decompose":
        from statsmodels.tsa.seasonal import seasonal_decompose

        decomposition = seasonal_decompose(xs, period=decompose_freq)
        trend, seasonality, residual = (
            decomposition.trend,
            decomposition.seasonal,
            decomposition.resid,
        )
        fig, ax = plt.subplots(4, 1, figsize=figsize)
        ax[0].plot(xs)
        ax[0].set_ylabel("original")
        ax[1].plot(trend)
        ax[1].set_ylabel("trend")
        ax[2].plot(seasonality)
        ax[2].set_ylabel("seasonality")
        ax[3].plot(residual)
        ax[3].set_ylabel("residual")
    elif type == "test":  # statistics and Dickey-Fuller test
        df = xs.to_frame()
        df["mean"] = xs.rolling(window).mean()
        df["var"] = xs.rolling(window).var()
        df["std"] = xs.rolling(window).std()
        df.plot(figsize=figsize, title="rolling mean and variance")
        from statsmodels.tsa.stattools import adfuller

        df_test = adfuller(xs.values, autolag="AIC")
        df_output = pd.Series(
            df_test[0:4],
            index=[
                "Test Statistic",
                "p-value",
                "#Lags Used",
                "Number of Observations Used",
            ],
        )
        for key, value in df_test[4].items():
            df_output["Critical Value (%s)" % key] = value
        print(df_output.head())
    else:
        raise Exception("invalid type %s" % type)
