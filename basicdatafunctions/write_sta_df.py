#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import os

import math
from fileinput import filename

def write_to_micaps3(sta0,filename = "a.txt", type = 1):
    dir = os.path.split(os.path.abspath(filename))[0]
    if os.path.isdir(dir):
        sta = sta0.reindex(columns =['lon','lat','height','dat'],fill_value=0)
        br = open(filename,'w')
        end = len(filename)
        start = max(0, end-16)
        str1=("diamond 3 " + filename[start:end] + "\n2018 01 01 08 " + str(type) +" 0 0 0 0\n1 " + str(len(sta)))
        br.write(str1);
        br.write(sta.to_string(header = False))
        br.close()
        return 0
    else:
        return 1