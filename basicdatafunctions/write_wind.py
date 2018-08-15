#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import os

import math
from fileinput import filename
import zlib
import netCDF4 as nc

def write_to_micaps11(wind, filename="a.txt"):
    dir = os.path.split(os.path.abspath(filename))[0]
    if os.path.isdir(dir):
        br = open(filename, 'w')
        end = len(filename)
        start = max(0, end-16)
        str1 = ("diamond 11 " + filename[start:end] + "\n2018 01 01 08 000 "
                + str(wind.dlon) + " " + str(wind.dlat) + " " + str(wind.slon) + " " + str(wind.elon) + " "
                + str(wind.slat) + " " + str(wind.elat) + " " + str(wind.nlon) + " " + str(wind.nlat))
        br.write(str1);
        for j in range(wind.nlat):
            br.write("\n");
            for i in range(wind.nlon):
                br.write(str(wind.u[j,i]) + " ");
        for j in range(wind.nlat):
            br.write("\n");
            for i in range(wind.nlon):
                br.write(str(wind.v[j,i]) + " ");
        br.close()
        return 0
    else:
        return 1