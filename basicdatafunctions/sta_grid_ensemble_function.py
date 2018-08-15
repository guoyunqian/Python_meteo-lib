#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
from mymethods.math import lon_lat_to_cartesian
from scipy.spatial import cKDTree
import basicdatas as bd
import basicdatafunctions as bf
import numpy as np

def get_nearby_sta_index_ensemble(sta, grid,nearNum = 1):
    grd_en = bd.grid_data_ensemble(grid,nearNum)
    xyz_sta =  lon_lat_to_cartesian(sta.ix[:,0], sta.ix[:,0],R = bd.ER)
    lon = np.arange(grd_en.nlon) * grd_en.dlon + grd_en.slon
    lat = np.arange(grd_en.nlat) * grd_en.dlat + grd_en.slat
    grid_lon,grid_lat = np.meshgrid(lon,lat)
    xyz_grid = lon_lat_to_cartesian(grid_lon.flatten(), grid_lat.flatten(),R = bd.ER)
    tree = cKDTree(xyz_sta)
    _, inds = tree.query(xyz_grid, k=nearNum)
    grd_en.dat = inds.reshape((nearNum,grd_en.nlat,grd_en.nlon))
    return grd_en