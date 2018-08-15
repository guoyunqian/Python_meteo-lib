#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import os
import time
import math
from fileinput import filename
def write_to_micaps3(sta,filename = "a.txt", type = 1):
    dir = os.path.split(os.path.abspath(filename))[0]
    if os.path.isdir(dir):
        br = open(filename,'w')
        end = len(filename)
        start = max(0, end-16)
        nsta =len(sta.index)
        str1=("diamond 3 " + filename[start:end] + "\n2018 01 01 08 " + str(type) +" 0 0 0 0\n1 " + str(nsta) + "\n")
        br.write(str1)
        br.close()
        dframe = sta.reindex(columns = ['lon','lat','alt','dat'],fill_value=1)
        dframe.to_csv(filename,mode='a',header=None,sep = "\t")
        return 0
    else:
        return 1