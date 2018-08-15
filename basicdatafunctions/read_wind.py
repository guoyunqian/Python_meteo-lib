#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import basicdatafunctions.grid_grid_function as ggf
import os
import zlib
import struct
import math

def read_from_micaps11(filename):
    if os.path.exists(filename):
        file = open(filename, 'r')
        str1 = file.read()
        file.close()
        strs = str1.split()
        dlon = float(strs[8]);
        dlat = float(strs[9]);
        slon = float(strs[10]);
        elon = float(strs[11]);
        slat = float(strs[12]);
        elat = float(strs[13]);
        wind = bd.wind_data(bd.grid(slon, dlon, elon, slat, dlat, elat))
        if len(strs) - 15 >= 2 * wind.nlon * wind.nlat:
            k = 16
            wind.u= (np.array(strs[k:(k + wind.nlon * wind.nlat)])).astype(float).reshape((wind.nlat,wind.nlon))
            k += wind.nlon * wind.nlat
            wind.v = (np.array(strs[k:(k + wind.nlon * wind.nlat)])).astype(float).reshape((wind.nlat, wind.nlon))
            wind.reset()
            return wind
        else:
            return None
    else:
        return None

def read_from_micaps2(filename):
    if os.path.exists(filename):
        file = open(filename, 'r')
        str1 = file.read()
        file.close()
        strs = str1.split()
        nsta = int(strs[8])
        dat_list = np.zeros((nsta,4))
        for i in range(nsta):
            k = 9 + i *10
            dat_list[i,0] = float(strs[k + 1])
            dat_list[i,1] = float(strs[k + 2])
            dat_list[i, 2] = float(strs[k + 8])
            dat_list[i, 3] = float(strs[k + 9])
        slon = min(dat_list[0,0],dat_list[-1,0])
        elon = max(dat_list[0,0],dat_list[-1,0])
        slat = min(dat_list[0,1],dat_list[-1,1])
        elat = max(dat_list[0,1],dat_list[-1,1])
        dlon = abs(dat_list[0,0] - dat_list[1,0])
        dlat = dlon
        grid = bd.grid(slon,dlon,elon,slat,dlat,elat)
        wind = bd.wind_data(grid)
        i_index = ((dat_list[:,0] - slon)/dlon).astype(int)
        j_index = ((dat_list[:,1] - slat)/dlat).astype(int)
        u = - np.sin(math.pi * dat_list[:,2] /180) * dat_list[:,3]
        v = - np.cos(math.pi * dat_list[:,2] /180) * dat_list[:,3]
        wind.u[j_index,i_index] = u
        wind.v[j_index,i_index] = v
        return wind
    else:
        return None

