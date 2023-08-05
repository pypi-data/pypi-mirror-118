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

from math import sqrt

import numpy as np
from numpy.random import standard_normal
from quantlet_streaming.stream import QLet


def seed(s):
    np.random.seed(s)


_seed = seed


@QLet
def random_walk(t=100, dt=0.25, s0=10.0, mu=0.0, sigma=0.1):
    """
    Geometric brownian motion. Each invocation yields a different motion.

    From Wikipedia:
    http://en.wikipedia.org/wiki/Geometric_Brownian_motion#Solving_the_SDE

    mu: drift factor
    sigma: volatility in %
    t: time span
    dt: lenght of steps
    s0: value of motion on step=0

    """

    # step: time step
    # w: Geometric Brownian Motion
    w = s0
    for step in np.arange(0, t, dt):
        w = max(0.001, w)
        yield dict(step=step, w=w)
        x = (
            w * (mu - 0.5 * sigma ** 2) * dt
            + (sigma * w) * sqrt(dt) * standard_normal()
        )
        w = x + w


@QLet
def brownian(iterable, seed=None, output="brownian", t=100,
             dt=0.25, s0=0.0, mu=0.0, sigma=0.1):
    """
    Geometric brownian motion. Each invocation yields a different motion.

    From Wikipedia:
    http://en.wikipedia.org/wiki/Geometric_Brownian_motion#Solving_the_SDE

    mu: drift factor
    sigma: volatility in %
    t: time span
    dt: lenght of steps
    s0: value of motion on step=0

    """

    # step: time step
    # w: Geometric Brownian Motion
    if seed is not None:
        _seed(seed)
    w = s0
    # step = 0
    for i in iterable:
        w = max(0.001, w)
        i[output] = w
        yield i
        x = (
            w * (mu - 0.5 * sigma ** 2) * dt
            + (sigma * w) * sqrt(dt) * standard_normal()
        )
        w = x + w


@QLet
def random_uniform(iterable, output="random_uniform", band=(-10, 10)):
    """
    Random walk based on a normal random distribution
    """
    last = np.random.uniform(band[0], band[1])
    for i in iterable:
        next = np.random.uniform(band[0], band[1])
        w = last + next
        i[output] = w
        yield i
        last = w
