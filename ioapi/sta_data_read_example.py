#!/usr/bin/env python
# coding=utf8

import ioapi.DataBlock_pb2 as DataBlock_pb2
import ioapi.GDS_data_service as GDS_data_service
import struct
import os
import time,datetime

#数据目录
directory = "SURFACE/RAIN01_NATIONAL"
#output_directory = "e:/NMC/nwp/t2m/"
output_directory = "J:/ec_t_2m/"
#初始化GDS客户端
#service = GDS_data_service.GDSDataService("10.181.22.103", 8080)
service = GDS_data_service.GDSDataService("10.20.65.64", 8080)
fileName = "20180722080000.000"
status, response = byteArrayResult = service.getData(directory, fileName)
ByteArrayResult = DataBlock_pb2.ByteArrayResult()
if status == 200:
    ByteArrayResult.ParseFromString(response)
    if ByteArrayResult is not None:
        byteArray = ByteArrayResult.byteArray
        discriminator =struct.unpack("4s",byteArray[:4])[0].decode("gb2312")
        print(discriminator)
        type = struct.unpack("h", byteArray[4:6])[0]
        print(type)
        description = struct.unpack("100s", byteArray[6:106])[0].decode("gb2312")
        level = struct.unpack("f", byteArray[106:110])[0]
        print(description)
        print(level)
        levelDescprition = struct.unpack("50s", byteArray[110:160])[0].decode("gb2312")
        print(levelDescprition)
        y, m, d, h, minute, second,timezone = struct.unpack("iiiiiii", byteArray[160:188])
        print(y)
        print(m)
        print(d)
        print(h)
        print(minute)
        print(second)
        print(timezone)
        extent = struct.unpack("100s", byteArray[188:288])[0].decode("gb2312")
        print(extent)
        nsta = struct.unpack("i", byteArray[288:292])[0]
        print(nsta)
        id_num = struct.unpack("h", byteArray[292:294])[0]
        print(id_num)
        id_tpye = {}
        for i in range(id_num):
            id_tpye[struct.unpack("h", byteArray[294+i*4:296+i*4])[0]] = struct.unpack("h", byteArray[296+i*4:298+i*4])[0]
        print(id_tpye)
        station_data_list = []
        index = 294+id_num*4

        type_lenght_dict = {1:1,2:2,3:4,4:4,5:4,6:8,7:1}
        type_str_dict = {1:'b',2:'h',3:'i',4:'l',5:'f',6:'d',7:'c'}

        for i in range(nsta):
            one_station_dat = []
            one_station_dat.append(struct.unpack("i", byteArray[index : index + 4])[0])
            index += 4
            one_station_dat.append(struct.unpack("f", byteArray[index: index + 4])[0])
            index += 4
            one_station_dat.append(struct.unpack("f", byteArray[index: index + 4])[0])
            index += 4
            value_num = struct.unpack("h", byteArray[index:index+2])[0]
            index += 2
            values = {}
            for j in range(value_num):
                id = struct.unpack("h", byteArray[index:index+2])[0]
                index += 2
                id_tpye0 = id_tpye[id]
                dindex = type_lenght_dict[id_tpye0]
                type_str = type_str_dict[id_tpye0]
                value = struct.unpack(type_str, byteArray[index:index+dindex])[0]
                index += dindex
                values[id] = value
            one_station_dat.append(values)
            print(one_station_dat)
            station_data_list.append(one_station_dat)