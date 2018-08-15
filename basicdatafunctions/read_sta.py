#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import os
import basicdatafunctions.sta_sta_function as ssf
from collections import OrderedDict
import ioapi.DataBlock_pb2 as DataBlock_pb2
import ioapi.GDS_data_service as GDS_data_service
import struct
from collections import OrderedDict
from pandas import DataFrame
import pandas as pd

def read_from_micaps1_2_8(filename,column,station = None):
    if os.path.exists(filename):
        df = pd.read_csv(filename, skiprows=2, sep="\s+", header=None, index_col=0)
        index_str = np.array(df.index.tolist()).astype("str")
        df = pd.DataFrame(df.values,index=index_str)
        sta1 = bd.sta_data(df, column)
        if(station is None):
            return sta1
        else:
            sta = ssf.recover(sta1, station)
            return sta
    else:
        return None


def read_from_micaps3(filename,station = None):
    if os.path.exists(filename):
        file = open(filename,'r')
        str1 = file.read()
        file.close()
        strs = str1.split()
        nline = int(strs[8])
        nregion = int(strs[11+nline])
        nstart=nline+2*nregion+14
        nsta=int((len(strs)-nstart)/5)
        str_array =np.delete(np.array(strs[nstart:]).reshape((nsta,5)),3,axis = 1)
        ids = str_array[:,0]
        dat = str_array[:,1:].astype("float32")
        sta1 = DataFrame(dat,index = ids,columns=['lon','lat','dat'])
        if (station is None):
            return sta1
        else:
            sta = ssf.recover(sta1,station)
            return sta
    else:
        return None

def read_from_gds(filename,element_id = None,station = None,service = None):
    try:
        if(service is None):service = GDS_data_service.service
        directory,fileName = os.path.split(filename)
        status, response = byteArrayResult = service.getData(directory, fileName)
        ByteArrayResult = DataBlock_pb2.ByteArrayResult()
        if status == 200:
            ByteArrayResult.ParseFromString(response)
            if ByteArrayResult is not None:
                byteArray = ByteArrayResult.byteArray
                nsta = struct.unpack("i", byteArray[288:292])[0]
                id_num = struct.unpack("h", byteArray[292:294])[0]
                id_tpye = {}
                for i in range(id_num):
                    element_id0 = struct.unpack("h", byteArray[294 + i * 4:296 + i * 4])[0]
                    id_tpye[element_id0] = struct.unpack("h", byteArray[296 + i * 4:298 + i * 4])[0]
                    if(element_id is None and element_id0 > 200 and element_id0 % 2 == 1):
                        element_id = element_id0
                station_data_dict = OrderedDict()
                index = 294 + id_num * 4
                type_lenght_dict = {1: 1, 2: 2, 3: 4, 4: 4, 5: 4, 6: 8, 7: 1}
                type_str_dict = {1: 'b', 2: 'h', 3: 'i', 4: 'l', 5: 'f', 6: 'd', 7: 'c'}

                for i in range(nsta):
                    one_station_dat = {}
                    one_station_id =struct.unpack("i", byteArray[index: index + 4])[0]
                    index += 4
                    one_station_dat['lon'] =struct.unpack("f", byteArray[index: index + 4])[0]
                    index += 4
                    one_station_dat['lat'] =(struct.unpack("f", byteArray[index: index + 4])[0])
                    index += 4
                    value_num = struct.unpack("h", byteArray[index:index + 2])[0]
                    index += 2
                    values = {}
                    for j in range(value_num):
                        id = struct.unpack("h", byteArray[index:index + 2])[0]
                        index += 2
                        id_tpye0 = id_tpye[id]
                        dindex = type_lenght_dict[id_tpye0]
                        type_str = type_str_dict[id_tpye0]
                        value = struct.unpack(type_str, byteArray[index:index + dindex])[0]
                        index += dindex
                        values[id] = value
                    if(element_id in values.keys()):
                        one_station_dat['dat'] =(values[element_id])
                        station_data_dict[one_station_id] = one_station_dat
                sta = pd.DataFrame(station_data_dict).T.ix[:,['lon','lat','dat']]
                return sta
        return None
    except:
        return None


