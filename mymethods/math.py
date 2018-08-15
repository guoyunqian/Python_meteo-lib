# coding: utf-8
import numpy as np
import math
def sigmoid(inputX):
    return 1.0/(1+np.exp(-inputX))
def earth_surface_dis(ax,ay,bx,by):
    sr=math.cos(ay*math.pi/180)
    d1=(ax-bx)*sr
    d2=ay-by
    dis1=math.sqrt(d1*d1+d2*d2)
    return dis1

def earth_surface_dis2(ax,ay,bx,by):
    sr=math.cos(ay*math.pi/180)
    d1=(ax-bx)*sr
    d2=ay-by
    dis2=d1*d1+d2*d2
    return dis2

def lon_lat_to_cartesian(lon, lat, R=1):
    """
    calculates lon, lat coordinates of a point on a sphere with
    radius R
    """
    lon_r = np.radians(lon)
    lat_r = np.radians(lat)
    xyz = np.zeros((len(lon), 3))
    xyz[:, 0] = R * np.cos(lat_r) * np.cos(lon_r)
    xyz[:, 1] = R * np.cos(lat_r) * np.sin(lon_r)
    xyz[:, 2] = R * np.sin(lat_r)
    return xyz


def get_rh_from_t_and_td(t,td):
    e_sw = 6.10695 * math.pow(10, 7.5927 * t/(240.727 + t))
    e = 6.10695 * math.pow(10, 7.5927 * td/(240.727 + td))
    rh = 100 * e / e_sw
    return rh