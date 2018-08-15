#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import basicdatafunctions as bf
import os
import zlib
import struct
from netCDF4 import Dataset
import time
import math
import ioapi.DataBlock_pb2 as DataBlock_pb2
import ioapi.GDS_data_service as GDS_data_service
import struct
import datetime


def read_from_micaps4(filename):
    try:
        if not os.path.exists(filename):
            print(filename + " is not exist")
            return None
        file = open(filename,'r')
        str1 = file.read()
        file.close()
        strs = str1.split()
        
        dlon = float(strs[9]);
        dlat = float(strs[10]);
        slon = float(strs[11]);
        elon = float(strs[12]);
        slat = float(strs[13]);
        elat = float(strs[14]);        
        grd = bd.grid_data(bd.grid(slon,dlon,elon,slat,dlat,elat))
        if len(strs) - 22 >= grd.nlon * grd.nlat :
            k=22
            grd.dat = (np.array(strs[k:])).astype(float).reshape((grd.nlat,grd.nlon))
            grd.reset()
            return grd
        else:
            return None
    except:
        print(filename + "'s format is wrong")
        return None

def read_grd_array_by_ctl(filename,ctl = None):
    if ctl is None:
        if os.path.exists(filename):
            ctl = read_ctl(filename)
            return read_grd_array_by_ctl(ctl.data_path,ctl)
    else:
        if os.path.exists(filename):
            data = np.fromfile(filename, dtype='f')
            data = data.reshape(ctl.nvar, ctl.nensemble, ctl.ntime, ctl.nlevel, ctl.nlat, ctl.nlon)
            #print(data.shape)
            grid = bd.grid(ctl.slon, ctl.dlon, ctl.elon, ctl.slat, ctl.dlat, ctl.elat)
            arr = [[[[] for t in range(ctl.ntime)] for n in range(ctl.nensemble)] for v in range(ctl.nvar)]
            for v in range(ctl.nvar):
                for n in range(ctl.nensemble):
                    for t in range(ctl.ntime):
                        for z in range(ctl.nlevel):
                            grd = bd.grid_data(grid)
                            grd.dat = data[v, n, t, z, :, :]
                            grd.reset()
                            arr[v][n][t].append(grd)
            return arr
    return None

def read_ctl(ctl_filename):
    if os.path.exists(ctl_filename):
        ctl = bd.ctl()
        file = open(ctl_filename, 'r')
        line = file.readline()
        strs = line.split()
        if strs[1].__contains__('^'):
            ctl.data_path = os.path.dirname(ctl_filename) +"\\"+ strs[1][1:]
        else:
            ctl.data_path = strs[1][1:]
        while line:
            strs = line.split()
            if strs[0].upper() == "XDEF":
                ctl.nlon = int(strs[1])
                ctl.slon = float(strs[3])
                ctl.dlon = float(strs[4])
            if strs[0].upper() == "YDEF":
                ctl.nlat = int(strs[1])
                ctl.slat = float(strs[3])
                ctl.dlat = float(strs[4])
            if strs[0].upper() == "ZDEF":
                ctl.nlevel = int(strs[1])
            if strs[0].upper() == "TDEF":
                ctl.ntime = int(strs[1])
            if strs[0].upper() == "VARS":
                ctl.nvar = int(strs[1])
            if(strs[0].upper() == "EDEF"):
                ctl.nensemble = int(strs[1])
            line = file.readline()
        ctl.elon = ctl.slon + ctl.dlon * (ctl.nlon-1)
        ctl.elat = ctl.slat + ctl.dlat * (ctl.nlat-1)
        return ctl
    else:
        return None

def read_from_compressed(filename):
    if(os.path.exists(filename)):
        file = open(filename, 'rb')
        bytes_compressed = file.read()
        file.close()
        bytes = zlib.decompress(bytes_compressed)
        head1 = np.frombuffer(bytes[0:24], dtype='float32')
        head2 = np.frombuffer(bytes[24:32], dtype='uint16')
        slon = head1[0]
        elon = head1[1]
        slat = head1[2]
        elat = head1[3]
        vmax = head1[4]
        vmin = head1[5]
        nlon_1 = head2[0] - 1
        nlat_1 = head2[1] - 1
        dlon = (elon - slon) / nlon_1
        dlat = (elat - slat) / nlat_1
        grade_num = head2[2]
        if(grade_num == 0):
            grd = bf.grid_data(bf.grid(slon, dlon, elon, slat, dlat, elat))
            grd.dat[:,:] = vmin
            return grd
        uint_8_or_16 = head2[3]
        uint_8_or_16_str = str(bin(uint_8_or_16)).replace("0b","").zfill(16)
        sparse_rate = int(math.pow(2,(15 - uint_8_or_16_str.index('1',1))/2))
        max_sparse_grid_num = int((nlon_1 / sparse_rate + 1) * (nlat_1 / sparse_rate + 1))
        grd = bf.grid_data(bf.grid(slon, dlon * sparse_rate, elon, slat, dlat * sparse_rate, elat))

        bn = 32
        k = 0
        #print(uint_8_or_16_str)
        if (uint_8_or_16_str[k:k+1] == '1'):
            grd.dat = np.frombuffer(bytes[bn:bn + max_sparse_grid_num * 2], dtype='uint16').reshape(grd.nlat,grd.nlon)
            bn += max_sparse_grid_num * 2
        else:
            grd.dat = np.frombuffer(bytes[bn:bn + max_sparse_grid_num], dtype='uint8').reshape(grd.nlat,grd.nlon)
            bn += max_sparse_grid_num
        k = uint_8_or_16_str.index('1',1)
        while(sparse_rate > 1):
            grd1 = bf.ggf.cubicInterpolation(grd, bf.grid(slon, grd.dlon / 2, elon, slat, grd.dlat / 2, elat))
            d_int = np.zeros((grd1.nlat,grd1.nlon))
            k += 1
            if (uint_8_or_16_str[k:k+1] == '1'):
                d_int_odd = np.frombuffer(bytes[bn:bn + grd.nlat *(grd.nlon - 1) * 2], dtype='int16').reshape(grd.nlat,grd.nlon - 1)
                bn += grd.nlat *(grd.nlon - 1) * 2
            else:
                d_int_odd = np.frombuffer(bytes[bn:bn + grd.nlat *(grd.nlon - 1)], dtype='int8').reshape(grd.nlat,grd.nlon - 1)
                bn += grd.nlat *(grd.nlon - 1)
            d_int[::2, 1::2] = d_int_odd

            k += 1
            if (uint_8_or_16_str[k:k+1] == '1'):
                d_int_even = np.frombuffer(bytes[bn:bn + (grd.nlat - 1) * grd1.nlon * 2], dtype='int16').reshape(grd.nlat - 1, grd1.nlon)
                bn += (grd.nlat - 1) * grd1.nlon * 2

            else:
                d_int_even = np.frombuffer(bytes[bn:bn + (grd.nlat - 1) * grd1.nlon], dtype='int8').reshape(grd.nlat - 1, grd1.nlon)
                bn += (grd.nlat - 1) * grd1.nlon
            d_int[1::2, :]  = d_int_even
            grd1.dat = np.rint(grd1.dat) - d_int
            grd = grd1
            sparse_rate /= 2
        grd.dat = grd.dat * (vmax - vmin) / grade_num + vmin
        return grd


def read_from_nc(filename,valueName = None):
    if os.path.exists(filename):
        f = Dataset(filename)
        lons = None
        lats = None
        for key in f.variables.keys():
            #print(key)
            if 'lon' in key.lower():
                lonName = str(key)
                lons = f.variables[lonName][:]
            elif 'lat' in key.lower():
                latName = key
                lats = f.variables[latName][:]
            elif 'time' not in key.lower():
                if(valueName is None):
                    valueName = key
        dlon = (lons[-1] - lons[0]) / (len(lons) - 1)
        dlat = (lats[-1] - lats[0]) / (len(lats) - 1)
        grd = bd.grid_data(bd.grid(lons[0],dlon,lons[-1],lats[0],dlat,lats[-1]))
        grd.dat = f.variables[valueName][:].T
        return grd


def read_from_gds(filename,service = None,grid = None):
    try:
        if(service is None):service = GDS_data_service.service
        directory,fileName = os.path.split(filename)
        status, response = byteArrayResult = service.getData(directory, fileName)
        ByteArrayResult = DataBlock_pb2.ByteArrayResult()
        if status == 200:
            ByteArrayResult.ParseFromString(response)
            if ByteArrayResult is not None:
                byteArray = ByteArrayResult.byteArray

                file_type = os.path.splitext(filename)
                if file_type[1] == '.AWX':
                    return explain_awx_bytes(byteArray)
                else:
                    #print(len(byteArray))
                    discriminator = struct.unpack("4s", byteArray[:4])[0].decode("gb2312")
                    t = struct.unpack("h", byteArray[4:6])
                    mName = struct.unpack("20s", byteArray[6:26])[0].decode("gb2312")
                    eleName = struct.unpack("50s", byteArray[26:76])[0].decode("gb2312")
                    description = struct.unpack("30s", byteArray[76:106])[0].decode("gb2312")
                    level, y, m, d, h, timezone, period = struct.unpack("fiiiiii", byteArray[106:134])
                    startLon, endLon, lonInterval, lonGridCount = struct.unpack("fffi", byteArray[134:150])
                    startLat, endLat, latInterval, latGridCount = struct.unpack("fffi", byteArray[150:166])
                    isolineStartValue, isolineEndValue, isolineInterval = struct.unpack("fff", byteArray[166:178])
                    gridCount = lonGridCount * latGridCount
                    description = mName.rstrip('\x00') + '_' + eleName.rstrip('\x00') + "_" + str(
                        level) + '(' + description.rstrip('\x00') + ')' + ":" + str(period)
                    if (gridCount == (len(byteArray) - 278) / 4):
                        if(startLat > 90):startLat = 90.0
                        if(startLat < -90) : startLat = -90.0
                        if(endLat > 90) : endLat = 90.0
                        if(endLat < -90): endLat = -90.0
                        grd = bd.grid_data(bd.grid(startLon,lonInterval,endLon,startLat,latInterval,endLat))
                        grd.dat = np.frombuffer(byteArray[278:], dtype='float32').reshape(grd.nlat,grd.nlon)
                        grd.reset()
                        if (grid is None):
                            return grd
                        else:
                            return bf.ggf.linearInterpolation(grd,grid)


    except Exception as e:
        print(e)
        return None

def read_from_awx(filename):
    if os.path.exists(filename):
        file = open(filename,'rb')
        byte_array = file.read()
        return explain_awx_bytes(byte_array)
    else:
        return None
def explain_awx_bytes(byteArray):
    sat96 = struct.unpack("12s", byteArray[:12])[0]
    levl = np.frombuffer(byteArray[12:30], dtype='int16').astype(dtype = "int32")
    formatstr = struct.unpack("8s", byteArray[30:38])[0]
    qualityflag = struct.unpack("h", byteArray[38:40])[0]
    satellite = struct.unpack("8s", byteArray[40:48])[0]
    lev2 = np.frombuffer(byteArray[48:104], dtype='int16').astype(dtype = "int32")

    recordlen = levl[4]
    headnum = levl[5]
    datanum = levl[6]
    timenum =lev2[0:5]
    nlon = lev2[7]
    nlat = lev2[8]
    range =lev2[12:16].astype("float32")
    slat = range[0]/100
    elat = range[1]/100
    slon = range[2]/100
    elon = range[3]/100

    #nintels=lev2[20:22].astype("float32")
    dlon = (elon - slon) / (nlon-1)
    dlat = (elat - slat) / (nlat-1)

    grd = bd.grid_data(bd.grid(slon, dlon, elon, slat, dlat, elat))

    colorlen = lev2[24]
    caliblen = lev2[25]
    geololen = lev2[26]

    #print(levl)
    #print(lev2)
    head_lenght = headnum * recordlen
    data_lenght = datanum * recordlen
    #print(head_lenght  + data_lenght)
    #print( data_lenght)
    #print(grd.nlon * grd.nlat)
    #headrest = np.frombuffer(byteArray[:head_lenght], dtype='int8')
    data_awx = np.frombuffer(byteArray[head_lenght:(head_lenght+data_lenght)], dtype='int8')
    #print(headrest)

    if colorlen<=0:
        calib = np.frombuffer(byteArray[104:(104+2048)], dtype='int16').astype(dtype="float32")
    else:
        #color = np.frombuffer(byteArray[104:(104+colorlen*2)], dtype='int16')
        calib = np.frombuffer(byteArray[(104+colorlen*2):(104+colorlen*2+ 2048)], dtype='int16').astype(dtype="float32")

    realcalib = calib /100.0
    realcalib[calib<0] = (calib[calib<0] + 65536) /100.0

    awx_index = np.empty(len(data_awx),dtype = "int32")
    awx_index[:] = data_awx[:]
    awx_index[data_awx <0] = data_awx[data_awx <0] +256
    awx_index *= 4
    real_data_awx = realcalib[awx_index]

    grd.dat = real_data_awx.reshape(grd.nlat,grd.nlon)
    grd.reset()
    return grd

