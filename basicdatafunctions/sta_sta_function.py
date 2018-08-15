#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-

import numpy as np
from copy import deepcopy
import basicdatas as bd
from mymethods.math import lon_lat_to_cartesian
from scipy.spatial import cKDTree
import math
from collections import OrderedDict
import pandas as pd

def recover(sta_from,sta_to):
    ids = sta_to.index.intersection(sta_from.index)
    sta_to1 = sta_to.drop(ids)
    sta =pd.concat([sta_from,sta_to1])
    sta = sta.ix[sta_to.index,:]
    return sta

def add(sta1,sta2):
    sta = sta1.copy()
    sta.ix[:,'dat'] = sta1.ix[:,'dat'] + sta2.ix[:,'dat']
    return sta

def mutiply(sta1,sta2):
    sta = sta1.copy()
    sta.ix[:,'dat'] = sta1.ix[:,'dat'] * sta2.ix[:,'dat']
    return sta

def sqrt(sta_from):
    sta = sta_from.copy()
    sta['dat'] = sta['dat'].map(lambda  x: x **0.5)
    return sta

def get_both_having_station(sta1,sta2):
    ids = sta1.index.intersection(sta2.index)
    sta = sta1.ix[ids,:]
    return sta

def get_one_having_station(sta1,sta2):
    ids = sta1.index.intersection(sta2.index)
    sta =pd.concat([sta1.drop(ids),sta2])
    return sta

def sta_to_sta_idw(sta0, station,effectR = 1000,nearNum = 16):
    sta1 = station.copy()
    xyz_sta0 = lon_lat_to_cartesian(sta0.ix[:,0], sta0.ix[:,1],R = bd.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta1.ix[:,0], sta1.ix[:,1],R = bd.ER)
    tree = cKDTree(xyz_sta0)
    d, inds = tree.query(xyz_sta1, k=nearNum)
    d += 1e-6
    w = 1.0 / d ** 2
    input_dat = sta0.ix[:,2]
    dat = np.sum(w * input_dat[inds], axis=1) / np.sum(w, axis=1)
    dat[:] = np.where(d[:,0] > effectR,0,dat[:])
    sta1.ix[:,2] = dat
    return sta1

def set_IV(sta_from):
    sta = sta_from.copy()
    sta.ix[sta['dat']<=0,2] = bd.IV
    return sta

def reset_IV_value(sta_from,value):
    sta = sta_from.reindex(sta_from.index,fill_value= value)
    sta.ix[sta['dat'] == bd.IV, 2] = value

    return sta

def remove_IV(sta):
    sta1 = sta[sta['dat'] != bd.IV]
    return sta1

def get_sta_in_grid(sta,grid):
    grid.reset()
    sta1 = sta[sta['lon']>=grid.slon]
    sta1 = sta1[sta1['lon'] <grid.elon]
    sta1 = sta1[sta1['lat'] >= grid.slat]
    sta1 = sta1 [sta1['lat'] < grid.elat]
    return sta1

def get_sta_in_value_range(sta,start,end):
    sta1 = sta[sta['dat'] >= start]
    sta1 = sta1[sta1['dat'] <end]
    return sta1

def remove_path_station(sta,station):
    ids = sta.index.intersection(station.index)
    sta1 = sta.drop(ids)
    return sta1