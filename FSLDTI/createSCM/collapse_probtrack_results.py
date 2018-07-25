#!/usr/bin/python

from numpy import genfromtxt

def collapse_probtrack_results(waytotal_file, matrix_file):
    with open(waytotal_file) as f:
        waytotal = int(f.read())
    data = genfromtxt(matrix_file, delimiter='  ')
    collapsed = data.sum(axis=0) / waytotal * 100.
    return collapsed