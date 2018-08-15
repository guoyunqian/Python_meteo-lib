#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
from scipy.ndimage import convolve
import basicdatafunctions.grid_wind_function
import math

def max_grid(grd1,grd2):
    if(grd1 is None):
        return grd2
    elif(grd2 is None):
        return grd1
    grd = deepcopy(grd1)
    arr = np.array([grd1.dat,grd2.dat])
    grd.dat = np.max(arr,axis =0)
    return grd

def expand_to_contain_another_grid(grd0,grid):
    grd0.reset()
    grid.reset()
    si = 0
    sj = 0
    ei = 0
    ej = 0
    if(grid.slon < grd0.grid.slon):
        si = int(math.ceil((grd0.grid.slon - grid.slon)/grd0.grid.dlon))
    if(grid.slat < grd0.grid.slat):
        sj = int(math.ceil((grd0.grid.slat - grid.slat)/grd0.grid.dlat))
    if(grid.elon > grd0.grid.elon):
        ei = int(math.ceil((-grd0.grid.elon + grid.elon)/grd0.grid.dlon))
    if(grid.elat > grd0.grid.elat):
        ej = int(math.ceil((-grd0.grid.elat + grid.elat)/grd0.grid.dlat))
    slon = grd0.grid.slon - si * grd0.grid.dlon
    slat = grd0.grid.slat - sj * grd0.grid.dlat
    elon = grd0.grid.elon + ei * grd0.grid.dlon
    elat = grd0.grid.elat + ej * grd0.grid.dlat
    grd1 = bd.grid_data(bd.grid(slon,grd0.grid.dlon,elon,slat,grd0.grid.dlat,elat))
    grd1.dat[sj:(sj + grd0.grid.nlat), si:(si + grd0.grid.nlon)] = grd0.dat[:, :]
    return grd1

def linearInterpolation(grd0,grid):
    if(grd0 is None): return None
    grd1 = grd0.copy()
    if(grd0.dlon * grd0.nlon >= 360):
        grd1 = bd.grid_data(bd.grid(grd0.slon,grd0.dlon,grd0.elon + grd0.dlon, grd0.slat,grd0.dlat,grd0.elat))
        grd1.dat[:,0:-1] = grd0.dat[:,:]
        grd1.dat[:,grd0.nlon] = grd0.dat[:,0]
    grd2 = bd.grid_data(grid)
    if(grd2.elon > grd1.elon or grd2.slon < grd1.slon or grd2.elat > grd1.elat or grd2.slat < grd1.slat):
        print("object grid is out range of original grid")
        grd2.dat = bd.IV
        return
    x = ((np.arange(grd2.nlon) * grd2 .dlon + grd2.slon - grd1.slon) / grd1.dlon)
    ig = x[:].astype(dtype = 'int16')
    dx = x - ig
    y = (np.arange(grd2.nlat) * grd2 .dlat + grd2.slat - grd1.slat) / grd1.dlat
    jg = y[:].astype(dtype = 'int16')
    dy = y[:] - jg
    ii,jj = np.meshgrid(ig,jg)
    ii1 = np.minimum(ii + 1, grd1.nlon-1)
    jj1 = np.minimum(jj + 1, grd1.nlat-1)
    ddx,ddy = np.meshgrid(dx,dy)
    c00 = (1 - ddx) * (1 - ddy)
    c01 = ddx * (1 - ddy)
    c10 = (1 - ddx) * ddy
    c11 = ddx * ddy
    grd2.dat = (c00 * grd1.dat[jj,ii] + c10 * grd1.dat[jj1,ii] +c01 * grd1.dat[jj,ii1] + c11 * grd1.dat[jj1,ii1])
    return grd2


def cubicInterpolation(grd1,grid):
    if (grd1 is None): return None
    grd2 = bd.grid_data(grid)
    if(grd2.elon > grd1.elon or grd2.slon < grd1.slon or grd2.elat > grd1.elat or grd2.slat < grd1.slat):
        grd2.dat = bd.IV
        return
    x = ((np.arange(grd2.nlon) * grd2 .dlon + grd2.slon - grd1.slon) / grd1.dlon)
    ig = x[:].astype(dtype = 'int16')
    dx = x - ig
    y = (np.arange(grd2.nlat) * grd2 .dlat + grd2.slat - grd1.slat) / grd1.dlat
    jg = y[:].astype(dtype = 'int16')
    dy = y[:] - jg
    ii, jj = np.meshgrid(ig, jg)
    for p in range(-1,3,1):
        iip = np.minimum(np.maximum(ii+p,0),grd1.nlon-1)
        fdx = cubic_f(p, dx)
        for q in range(-1,3,1):
            jjq = np.minimum(np.maximum(jj+q,0),grd1.nlat-1)
            fdy = cubic_f(q,dy)
            fdxx,fdyy = np.meshgrid(fdx,fdy)
            fdxy = fdxx * fdyy
            grd2.dat += fdxy * grd1.dat[jjq,iip]
    return grd2

def cubic_f(n, dx):
    if (n == -1):
        return -dx * (dx - 1) * (dx - 2) / 6
    elif (n == 0):
        return (dx + 1) * (dx - 1) * (dx - 2) / 2
    elif (n == 1):
        return -(dx + 1) * dx * (dx - 2) / 2
    else:
        return (dx + 1) * dx * (dx - 1) / 6

def get_flowed_grid(grd,wind):
    flowed_grid = grd.copy()
    i = np.arange(grd.nlon)
    j = np.arange(grd.nlat)
    ii,jj = np.meshgrid(i,j)
    start_ii = ii - wind.u
    start_jj = jj - wind.v
    ix = start_ii.astype(dtype= 'int16')
    jy = start_jj.astype(dtype= 'int16')
    dx = start_ii - ix
    dy = start_jj - jy
    ix[ix<0] = 0
    ix[ix>grd.nlon-2] = grd.nlon -2
    jy[jy<0] = 0
    jy[jy >grd.nlat -2] = grd.nlat - 2
    ix1 = ix + 1
    jy1 = jy + 1
    temp1 = (1 - dx) * grd.dat[jy,ix] + dx * grd.dat[jy,ix1]
    temp2 = (1 - dx) * grd.dat[jy1,ix] + dx * grd.dat[jy1,ix1]
    flowed_grid.dat = (1 - dy) * temp1 +dy * temp2
    return flowed_grid

def optical_flow(grd1,grd2,delta_step = 1):
    previous=grd1.copy()
    current=grd2.copy()
    for n in range(delta_step):
        wind= basicdatafunctions.grid_wind_function.get_flow_wind_from_2grid(previous,current)
        forecast=get_flowed_grid(current,wind)
        previous = current.copy()
        current = forecast.copy()
    return forecast