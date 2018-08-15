#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-

import numpy as np
from copy import deepcopy
import basicdatas as bd
import basicdatafunctions as bf
import pandas as pd

def transform(grd):
    grid_num = grd.nlon * grd.nlat
    x = np.arange(grd.nlon) * grd.dlon + grd.slon
    y = np.arange(grd.nlat) * grd.dlat + grd.slat
    grid_x,grid_y = np.meshgrid(x,y)
    dat = np.empty((grid_num,3))
    ids = np.arange(grid_num)
    dat[:,0] = grid_x.reshape(-1)
    dat[:,1] = grid_y.reshape(-1)
    dat[:,2] = grd.dat.reshape(-1)
    sta = pd.DataFrame(dat,index=ids,columns=['lon','lat','dat'])
    return sta

def linearInterpolation(grd,sta):
    sta1 = bf.ssf.get_sta_in_grid(sta,grd.grid)
    sta1['dat'] = 0
    ig = ((sta1.ix[:,0] - grd.slon) // grd.dlon).astype(dtype = 'int16')
    jg = ((sta1.ix[:,1] - grd.slat) // grd.dlat).astype(dtype = 'int16')
    dx = (sta1.ix[:,0] - grd.slon) / grd.dlon - ig
    dy = (sta1.ix[:,1] - grd.slat) / grd.dlat - jg
    c00 = (1 - dx) * (1 - dy)
    c01 = dx * (1 - dy)
    c10 = (1-dx) * dy
    c11 = dx * dy
    sta1['dat']= c00 * grd.dat[jg,ig] + c01 * grd.dat[jg,ig+1] + c10 * grd.dat[jg+1,ig] + c11 * grd.dat[jg+1,ig+1]
    return sta1

def cubicInterpolation(grd,sta):
    sta1 = bf.ssf.get_sta_in_grid(sta,grd.grid)
    sta1['dat'] = 0
    ig = ((sta1.ix[:,0] - grd.slon) // grd.dlon).astype(dtype = 'int16')
    jg = ((sta1.ix[:,1] - grd.slat) // grd.dlat).astype(dtype = 'int16')
    dx = (sta1.ix[:,0] - grd.slon) / grd.dlon - ig
    dy = (sta1.ix[:,1] - grd.slat) / grd.dlat - jg

    for p in range(-1,3,1):
        iip = np.minimum(np.maximum(ig+p,0),grd.nlon-1)
        fdx = cubic_f(p, dx)
        for q in range(-1,3,1):
            jjq = np.minimum(np.maximum(jg+q,0),grd.nlat-1)
            fdy = cubic_f(q,dy)
            fdxy = fdx * fdy
            sta1['dat'] +=  fdxy * grd.dat[jjq,iip]
    return sta1

def cubic_f(n, dx):
    if (n == -1):
        return -dx * (dx - 1) * (dx - 2) / 6
    elif (n == 0):
        return (dx + 1) * (dx - 1) * (dx - 2) / 2
    elif (n == 1):
        return -(dx + 1) * dx * (dx - 2) / 2
    else:
        return (dx + 1) * dx * (dx - 1) / 6