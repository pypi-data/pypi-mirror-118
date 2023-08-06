# -*- encoding: utf-8 -*-


import numpy as _np


def scale(input_: _np.ndarray, domain, range):
    """
    domain and range are of the format [min, max]
    """
    return range[0] + (((range[1] - range[0]) / (domain[1] - domain[0])) * (input_ - domain[0]))


def stack(inputs):
    return _np.vstack(inputs).T
