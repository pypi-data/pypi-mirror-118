# -*- encoding: utf-8 -*-


import numpy as _np

"""
input should be 2xN ndarray
domain and range should be 2x2 ndarray
"""


def scale(input_: _np.ndarray, domain, range):
    return range[0] + (((range[1] - range[0]) / (domain[1] - domain[0])) * (_np.array(input_) - domain[0]))


def stack(inputs):
    return _np.vstack(inputs).T
