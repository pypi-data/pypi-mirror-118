# -*- encoding: utf-8 -*-


import numpy as _np
import h5py as _h5py


def read_csv(file_, column, skip_header=0):
    return _np.genfromtxt(file_, delimiter=",", skip_header=skip_header,
                          usecols=(column))


def read_hdf5(file_, data_path):
    with _h5py.File(file_, "r") as hdf5_file:
        data = hdf5_file[data_path][:]
    return data
