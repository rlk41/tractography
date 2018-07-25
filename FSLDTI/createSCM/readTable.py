#!/usr/bin/python


import numpy as np

def readTable(tbl):
    data = np.loadtxt(tbl, delimiter=',', skiprows=1,
                      dtype=np.dtype([
                          ('subunit',    'i4'),
                          ('name',       'U16'),
                          ('x',          'i4'),
                          ('y',          'i4'),
                          ('z',          'i4')]))

    return data

