#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import basicdatas as bd
import numpy as np

def get_u(wind):
    grd = bd.grid_data(wind.grid)
    grd.dat[:,:] = wind.u[:,:]
    return grd

def get_v(wind):
    grd = bd.grid_data(wind.grid)
    grd.dat[:,:] = wind.v[:,:]
    return grd

def get_wind_speed(wind):
    grd = bd.grid_data(wind.grid)
    grd.dat = np.power((np.power(wind.v,2) + np.power(wind.u,2)),0.5)
    return grd