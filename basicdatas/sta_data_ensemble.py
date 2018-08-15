#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
def sta_data_ensemble(sta,value_num):
    dat_strs = ['lon','lat']
    for i in range(value_num):
        dat_strs.append(str(i))
    return sta.reindex(columns = dat_strs)