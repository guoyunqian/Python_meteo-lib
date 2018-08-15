#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import datetime as datetime
import os as os
import numpy as np

def get_path(dir,time,dt = None,dt_cell = "hour"):
    if(dt is not None):
        if(not type(dt) == type(1)):
            if(dt_cell.lower()=="hour"):
                dt = int(dt.total_seconds() / 3600)
            elif(dt_cell.lower()=="minute"):
                dt = int(dt.total_seconds() / 60)
            elif(dt_cell.lower()=="day"):
                dt = int(dt.total_seconds() / (24*3600))
            else:
                dt = int(dt.total_seconds())
    else:
        dt = 0
    cdt3 = '%03d' % dt
    cdt4 = '%04d' % dt
    dir1 = dir.replace("TTTT",cdt4).replace("TTT",cdt3)

    y4 = time.strftime("%Y")
    y2 = y4[2:]
    mo = time.strftime("%m")
    dd = time.strftime("%d")
    hh = time.strftime("%H")
    mi = time.strftime("%M")
    ss = time.strftime("%S")
    dir1 = dir1.replace("YYYY",y4).replace("YY",y2).replace("MM",mo).replace("DD",dd).replace("HH",hh).replace("FF",mi).replace("SS",ss)
    return dir1


def creat_path(path):
    [dir,filename] = os.path.split(path)
    if(not os.path.exists(dir)):
        os.makedirs(dir)

def str_to_time(str0):
    return datetime.datetime.strptime(str0, '%Y%m%d%H%M')

def get_time_of_path(path_model,path):
    yy_index = path_model.find("YYYY")
    if  yy_index < 0:
        yy_index = path_model.find("YY")
        yy = int(path[yy_index: yy_index + 2])
    else:
        yy = int(path[yy_index: yy_index+4])
    mm_index = path_model.find("MM")
    mm = int(path[mm_index:mm_index+2])
    dd_index = path_model.find("DD")
    dd = int(path[dd_index:dd_index + 2])
    hh_index = path_model.find("HH")
    hh = int(path[hh_index:hh_index + 2])
    ff_index = path_model.find("FF")
    ff = int(path[ff_index:ff_index + 2])
    ss_index = path_model.find("SS")
    ss = int(path[ss_index:ss_index + 2])
    return datetime.datetime(yy,mm,dd,hh,ff,ss)

def get_dir_of_time(path_model,time):
    dir = os.path.split(get_path(path_model,time))[0]
    return dir

def get_path_list_of_time(path_model,time):
    dir = get_dir_of_time(path_model,time) +"/"
    path_list = os.listdir(dir)
    for i in range(len(path_list)):
        path_list[i] = dir  + path_list[i]
    return path_list

def get_time_nearest_path(path_model,time,max_seconds,path_list = None):
    if(path_list is None):
        path_list = get_path_list_of_time(path_model,time)
    dt_min = max_seconds
    nearest_path = None
    for path in path_list:
        time1 = get_time_of_path(path_model,path)
        dt = abs((time1 - time).total_seconds())
        if(dt < dt_min):
            dt_min = dt
            nearest_path = path
    return nearest_path
