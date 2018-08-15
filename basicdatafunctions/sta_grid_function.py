#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-

from scipy.interpolate import griddata
import numpy as np
import basicdatas as bd
import basicdatafunctions.grid_grid_function as ggf
from scipy.spatial import cKDTree
from mymethods.math import lon_lat_to_cartesian
from mymethods.frprmn2 import frprmn2
import basicdatafunctions.sta_sta_function as ssf
import math

def transform(sta):
    slon = np.min(sta.ix[:,0])
    elon = np.max(sta.ix[:,0])
    slat = np.min(sta.ix[:,1])
    elat = np.max(sta.ix[:,1])
    nsta = len(sta.index)
    for i in range(nsta-1):
        dlon = sta.ix[i,0] - sta.ix[i+1,0]
        if dlon != 0:
            dlon = math.fabs(dlon)
            break
    for i in range(nsta-1):
        dlat = sta.ix[i,1] - sta.ix[i+1,1]
        if dlat != 0:
            dlat = math.fabs(dlat)
            break
    grd = bd.grid_data(bd.grid(slon,dlon,elon,slat,dlat,elat))
    ig = ((sta.ix[:,0] - grd.slon) // grd.dlon).astype(dtype = 'int16')
    jg = ((sta.ix[:,1] - grd.slat) // grd.dlat).astype(dtype = 'int16')
    grd.dat[jg,ig] = sta.ix[:,2]
    return grd

def sta_to_grid_cubic(sta, grid, background = None):
    grd = bd.grid_data(grid)
    points = sta.ix[:,0:2]
    values = sta.ix[:,2]
    x = np.arange(grd.nlon) * grd.dlon + grd.slon
    y = np.arange(grd.nlat) * grd.dlat + grd.slat
    grid_x,grid_y = np.meshgrid(x,y)
    dat_cubic = griddata(points, values, (grid_x, grid_y), method='cubic')
    if(background is None):
        dat_near = griddata(points, values, (grid_x, grid_y), method='nearest')
        grd.dat = np.where(np.isnan(dat_cubic),dat_near,dat_cubic)
    else:
        bg = ggf.linearInterpolation(background,grid)
        grd.dat = np.where(np.isnan(dat_cubic), bg.dat, dat_cubic)
    return grd

def sta_to_grid_linear(sta, grid, background = None):
    grd = bd.grid_data(grid)
    points = sta.ix[:,0:2]
    values = sta.ix[:,2]
    x = np.arange(grd.nlon) * grd.dlon + grd.slon
    y = np.arange(grd.nlat) * grd.dlat + grd.slat
    grid_x,grid_y = np.meshgrid(x,y)
    dat_linear = griddata(points, values, (grid_x, grid_y), method='linear')
    if(background is None):
        dat_near = griddata(points, values, (grid_x, grid_y), method='nearest')
        grd.dat = np.where(np.isnan(dat_linear),dat_near,dat_linear)
    else:
        bg = ggf.linearInterpolation(background,grid)
        grd.dat = np.where(np.isnan(dat_linear), bg.dat, dat_linear)
    return grd


def sta_to_grid_idw(sta, grid,background = None,effectR = 1000,nearNum = 16):
    grd = bd.grid_data(grid)
    xyz_sta =  lon_lat_to_cartesian(sta.ix[:,0], sta.ix[:,1],R = bd.ER)
    lon = np.arange(grd.nlon) * grd.dlon + grd.slon
    lat = np.arange(grd.nlat) * grd.dlat + grd.slat
    grid_lon,grid_lat = np.meshgrid(lon,lat)
    xyz_grid = lon_lat_to_cartesian(grid_lon.flatten(), grid_lat.flatten(),R = bd.ER)
    tree = cKDTree(xyz_sta)
    d, inds = tree.query(xyz_grid, k=nearNum)
    d += 1e-6
    w = 1.0 / d ** 2
    input_dat = sta.ix[:,2]
    dat = np.sum(w * input_dat[inds], axis=1) / np.sum(w, axis=1)
    bg = bd.grid_data(grid)
    if(background is not None):
        bg = ggf.linearInterpolation(background,grid)
    bg_dat = bg.dat.flatten()
    dat = np.where(d[:,0] > effectR,bg_dat,dat)
    grd.dat = dat.reshape((grd.nlat,grd.nlon))
    return grd


def sta_to_grid_oa2(sta0,background,sm = 1,effect_R = 1000,rate_of_model = 0):
    sta = ssf.remove_IV(sta0)
    sta = ssf.get_sta_in_grid(sta,background.grid)
    grd = background.copy()
    ig = ((sta.ix[:,0] - grd.slon) // grd.dlon).astype(dtype = 'int16')
    jg = ((sta.ix[:,1] - grd.slat) // grd.dlat).astype(dtype = 'int16')
    dx = (sta.ix[:,0] - grd.slon) / grd.dlon - ig
    dy = (sta.ix[:,1] - grd.slat) / grd.dlat - jg
    c00 = (1 - dx) * (1 - dy)
    c01 = dx * (1 - dy)
    c10 = (1-dx) * dy
    c11 = dx * dy
    lat = np.arange(grd.nlat) * grd.dlat + grd.slat
    sr = 1/np.power(np.cos(lat*math.pi/180),4)
    def targe(x):
        grdv =  x.reshape(grd.nlat,grd.nlon)
        dx = grdv[:,:-2] + grdv[:,2:] - 2 * grdv[:,1:-1]
        cost1 = np.sum(dx * dx)
        dy = grdv[:-2,:] + grdv[2:,:] - 2 * grdv[1:-1,:]
        dy2 = dy * dy
        sum_dy = np.sum(dy2,axis=1)
        cost1 = cost1 + np.dot(sum_dy,sr[1:-1])

        sta_g = c00 * grd.dat[jg, ig] + c01 * grd.dat[jg, ig + 1] + c10 * grd.dat[jg + 1, ig] + c11 * grd.dat[
            jg + 1, ig + 1]
        error = sta.ix[:,2] - sta_g
        cost2 = np.sum(error * error)
        cost = sm * cost1 + cost2
        return cost

    def grads(x):
        grdv = x.reshape(grd.nlat,grd.nlon)
        g1 = np.zeros(grdv.shape)
        dx = 2 * (grdv[:,:-2] + grdv[:,2:] - 2 * grdv[:,1:-1])
        g1[:,:-2] = dx
        g1[:,2:] += dx
        g1[:,1:-1] -= 2*dx

        sr_expend = np.tile(sr[1:-1],[grd.nlon,1]).T
        dy = 2 *(grdv[:-2,:] + grdv[2:,:] - 2 * grdv[1:-1,:])
        dy_sr = dy * sr_expend
        g1[:-2,:] += dy_sr
        g1[2:,:] += dy_sr
        g1[1:-1,:] -= 2 * dy_sr

        g2 = np.zeros(grdv.shape)
        sta_g = c00 * grd.dat[jg, ig] + c01 * grd.dat[jg, ig + 1] + c10 * grd.dat[jg + 1, ig] + c11 * grd.dat[jg + 1, ig + 1]
        d = 2 * (sta_g - sta.ix[:,2])
        g2[jg,ig] += d * c00
        g2[jg,ig + 1]  += d * c01
        g2[jg+1,ig] += d * c10
        g2[jg+1,ig+1] += d * c11
        g = sm * g1 + g2
        return g.reshape(-1)

    x = grd.dat.reshape(-1)
    x_oa = frprmn2(x, targe, grads)
    grd = bd.grid_data(grd.grid)
    grd.dat = x_oa.reshape(grd.nlat,grd.nlon)
    return grd
