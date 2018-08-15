#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-

import numpy as np
from copy import deepcopy
import basicdatas as bd
import datetime

def timelist_to_sta(tL,start=None,end=None):
    ymd_start = -1
    hms_start = -1
    ymd_end = 21000101
    hms_end = 235959
    if(start is not None):
        ymd_start = start.year * 10000 + start.month * 100 + start.day
        hms_start = start.hour * 10000 + start.minute *100 + start.second
    if(end is not None):
        ymd_end = end.year * 10000 + end.month * 100 + end.day
        hms_end = end.hour * 10000 + end.minute *100 + end.second
    k = 0

    id_during = np.where(tL.dat[:,0] >= ymd_start and tL.dat[:,1] >= hms_start and tL.dat[:,0] < ymd_end and tL.dat[:,1] < end)
    ids = np.arange(len(id_during))
    dat = tL.dat[id_during,2:]
    sta = bd.sta_data({},ids,dat)
    return sta