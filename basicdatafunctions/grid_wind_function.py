# -*- coding:UTF-8 -*-
import cv2
import numpy as np
import basicdatafunctions as bf

def get_flow_wind_from_2grid(grd1,grd2):
    wind = bf.wind_data(grd1.grid)
    flow = cv2.calcOpticalFlowFarneback(grd1.dat, grd2.dat, None, 0.5, 5, 50, 5, 1, 1.0, 0)
    wind.u = flow[:,:,0]
    wind.v = flow[:,:,1]
    return wind