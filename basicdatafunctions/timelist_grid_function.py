#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-

import numpy as np
from copy import deepcopy
import basicdatas as bd
from basicdatafunctions.timelist_sta_function import timelist_to_sta
import datetime
import math
import mymethods as mymethod



def timelist_to_grid_nearHappen(grid,tL,R=0.2,start=None,end=None):
    sta = timelist_to_sta(tL, start, end)
    grd = bd.grid_data(grid)
    yN = int(R/grid.dlat)+1
    minD = grid.dlat * grid.dlat/(R*R)

    for k in range(sta.num):
        sr = math.cos(sta.dat[k,2]*math.pi/180)
        sr2 = sr*sr
        xN = int(yN/sr)
        jg = int(round((sta.dat[k,2] - grd.slat)/grd.dlat))
        ig = int(round((sta.dat[k,1] - grd.slon)/grd.dlat))
        maxp = min(ig + xN, grd.nlon) - ig
        minp = max(ig - xN, 0) - ig
        maxq = min(jg + yN, grd.nlat) - jg
        minq = max(jg - yN, 0) -jg
        for p in range(minp,maxp):
            p2 = p*p *sr2
            for q in range(minq,maxq):
                dense = 1/(p2 + q * q + 0.0001)
                if(dense >= minD):
                    grd.dat[jg+q,ig+p] += dense
    grd.dat[grd.dat >= 0.5] = 1
    grd.dat[grd.dat < 1] = 0
    return grd