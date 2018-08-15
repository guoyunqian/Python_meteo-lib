#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy

class grid_data_ensemble:
    def __init__(self, grid0, en_size):
        self.en_size = en_size
        self.grid = deepcopy(grid0)
        self.slon = grid0.slon
        self.dlon = grid0.dlon
        self.elon = grid0.elon
        self.slat = grid0.slat
        self.dlat = grid0.dlat
        self.elat = grid0.elat
        self.nlon = grid0.nlon
        self.nlat = grid0.nlat
        self.dat = np.zeros([en_size,grid0.nlat,grid0.nlon])

    def tostring(self):
        str1 = self.grid.tostring() + "en_size:" + str(self.en_size)
        str2 = "dat[0,0,0]: " + str(self.dat[0,0,0]) + "\ndat[0,nlat-1,0]: " + str(self.dat[0,self.nlat-1,0]) + "\ndat[0,0,nlon-1]: " + str(self.dat[0,0,self.nlon-1]) + "\ndat[0,nlat-1,nlon-1]: " + str(self.dat[0,self.nlat-1,self.nlon-1]) + "\n"
        return str1 + str2

    def copy(self):
        return deepcopy(self)