#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
from mymethods.math import lon_lat_to_cartesian
from scipy.spatial import cKDTree
import basicdatas as bd
import basicdatafunctions as bf
import numpy as np

def get_nearby_sta_index_ensemble(sta_to,nearNum = 100,sta_from = None):
    if(sta_to is None):
        return None
    sta_ensemble = bd.sta_data_ensemble(sta_to,nearNum)
    if(sta_from is None):
        sta_from = sta_to.copy()
    xyz_sta0 = lon_lat_to_cartesian(sta_to.ix[:,0], sta_to.ix[:,1],R = bd.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta_from.ix[:,0], sta_from.ix[:,1],R = bd.ER)
    tree = cKDTree(xyz_sta0)
    _,indexs = tree.query(xyz_sta1, k=nearNum)
    sta_ensemble.ix[:,2:] = indexs
    return sta_ensemble

def get_nearby_sta_value_ensemble(sta_to,nearNum = 100,sta_from = None):
    if(sta_to is None):
        return None
    sta_ensemble = bd.sta_data_ensemble(sta_to, nearNum)
    if(sta_from is None):
        sta_from = sta_to.copy()
    xyz_sta0 = lon_lat_to_cartesian(sta_to.ix[:,0], sta_to.ix[:,1],R = bd.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta_from.ix[:,0], sta_from.ix[:,1],R = bd.ER)
    tree = cKDTree(xyz_sta0)
    _, indexs = tree.query(xyz_sta1, k=nearNum)
    input_dat = sta_from.ix[:,2]
    sta_ensemble.ix[:,2:] = input_dat[indexs]
    return sta_ensemble

def get_nearby_sta_dis_ensemble(sta_to,nearNum = 100,sta_from = None):
    if(sta_to is None):
        return None
    sta_ensemble = bd.sta_data_ensemble(sta_to,nearNum)
    if(sta_from is None):
        sta_from = sta_to.copy()
    xyz_sta0 = lon_lat_to_cartesian(sta_to.ix[:,0], sta_to.ix[:,1],R = bd.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta_from.ix[:,0], sta_from.ix[:,1],R = bd.ER)
    tree = cKDTree(xyz_sta0)
    d, _ = tree.query(xyz_sta1, k=nearNum)
    sta_ensemble.ix[:, 2:] = d
    return sta_ensemble



