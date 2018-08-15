#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
import math

def get_mean_of_grid(grd):
    return np.mean(np.mean(grd.dat))

def get_var_of_grid(grd):
    grid_mean = get_mean_of_grid(grd)
    d2 = np.power(grd.dat - grid_mean,2)
    var2 = np.mean(np.mean(d2))
    return math.sqrt(var2)
