#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import  pygrib
import os
import basicdatas as bd

def read_from_grib2(filename,valueName,typeOfLevel = None, level = None):
    if os.path.exists(filename):
        gribs = pygrib.open(filename)

        if(level is None):
            grib = gribs.select(name=valueName,typeOfLevel= 'surface')[0]

        else:
            grib = gribs.select(shortName=valueName, typeOfLevel= typeOfLevel, level= level)[0]
        if (grib is not None):
            latlons = grib.latlons()
            lats = latlons[0][:, 0]
            lons = latlons[1][0, :]
            grd = bd.grid_data(bd.grid(lons[0], lons[1] - lons[0], lons[-1], lats[0], lats[1] - lats[0], lats[-1]))
            grd.dat = grib.values
            print(grd.nlon)
            print(grd.nlat)
            print(grd.dat.shape)
            grd.reset()
            return grd