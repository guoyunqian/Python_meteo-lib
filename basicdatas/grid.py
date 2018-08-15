#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import math
from copy import deepcopy

class grid:
    def __init__(self, slon,dlon,elon,slat,dlat,elat):
        self.slon = slon
        self.dlon = dlon
        self.elon = elon
        self.slat = slat
        self.dlat = dlat
        self.elat = elat
        nlon = 1 + (elon - slon) / dlon
        error = abs(round(nlon) - nlon)
        if(error>0.01):
            self.nlon = math.ceil(nlon)
        else:
            self.nlon = int(round(nlon))
        self.elon = self.slon + (nlon -1) * dlon

        nlat = 1 + (elat - slat) / dlat
        error = abs(round(nlat) - nlat)
        if(error>0.01):
            self.nlat = math.ceil(nlat)
        else:
            self.nlat = int(round(nlat))
        self.elat = self.slat + (nlat - 1) * dlat

    def tostring(self):
        str1 ="nlon: " + str(self.nlon) + "    nlat: " + str(self.nlat) + '\nslon: ' + str(self.slon) + "    dlon: " + str(self.dlon) + "    elon: " + str(self.elon) + "\nslat: " + str(self.slat) + "    dlat: " + str(self.dlat) + "    elat: " + str(self.elat) + "\n"
        return str1

    def copy(self):
        return deepcopy(self)

    def reset(self):
        if (self.dlon > 0 and self.dlat > 0):
            return
        dat1 = None
        if (self.dlat < 0):
            tran = self.slat
            self.slat = self.elat
            self.elat = tran
            self.dlat = abs(self.dlat)
        if (self.dlon < 0):
            tran = self.slon
            self.slon = self.elon
            self.elon = tran
            self.dlon = abs(self.dlon)
        return

