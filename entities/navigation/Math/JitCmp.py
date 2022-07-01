import math

import numpy as np
from numba import jit, float32, boolean, int32


@jit(float32(float32[:], float32[:]), nopython=True, cache=True)
def distance(a, b) -> float:
    c = (b - a)
    # print(type(c))
    d = c ** 2
    # dx = b[0] - a[0]
    # dy = b[1] - a[1]
    # (dx * dx + dy * dy) ** 0.5

    return np.sqrt(np.sum(d))


@jit(float32(float32[:]), nopython=True, cache=True)
def length(a) -> float:
    b = a ** 2
    c = np.sum(b)
    return np.sqrt(c)


@jit(float32[:](float32[:], float32[:]), nopython=True, cache=True)
def add(a, b):
    return a + b


@jit(float32[:](float32[:], float32[:]), nopython=True, cache=True)
def sub(a, b):
    return a - b


# @classmethod
# @jit(forceobj=True)
# def hash(cls, a: np.ndarray):
#    return hash((a[0], a[1]))


@jit(boolean(float32[:], float32[:]), nopython=True, cache=True)
def equals(a, b):
    return np.all(a == b)


@jit(float32[:](float32[:]), nopython=True, cache=True)
def uniform(a):
    return a / length(a)


@jit(int32(float32[:]), nopython=True, cache=True)
def angle(a):
    return math.floor(math.atan2(a[0], a[1]) * (180 / math.pi))


@jit(float32[:](float32[:], float32[:], float32, float32), nopython=True, cache=True)
def update(p, d, s, t):
    return p + (d * s * t)


@jit(float32[:](float32[:], float32[:]), nopython=True, cache=True)
def direction(a, b):
    c = (b - a)
    return c / length(c)
