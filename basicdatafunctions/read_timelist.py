#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import os

from itertools import cycle
from datetime import datetime
def read_from_txt(filename):
    if os.path.exists(filename):
        file = open(filename)
        line = file.readline()
        list = []
        while line:
            #print(line)
            strs = line.split()
            ymd=[]
            one_data =[]
            if(len(strs)==9 and strs[0].isdigit() and strs[1].isdigit() and strs[2].isdigit()):
                one_data.append(int(strs[0]) * 10000 + int(strs[1]) * 100 + int(strs[2]))
                one_data.append(int(strs[3]) * 10000 + int(strs[4]) * 100 + int(strs[5]))
                one_data.append(float(strs[6]))
                one_data.append(float(strs[7]))
                one_data.append(float(strs[8]))
            elif(len(strs)==5):
                ymd = strs[0].split('/')
                if(len(ymd) ==3 and ymd[0].isdigit() and ymd[1].isdigit() and ymd[2].isdigit()):
                    one_data.append(int(ymd[0])*10000+int(ymd[1])*100+int(ymd[2]))
                    hms = strs[1].split(':')
                    if(len(hms)==2): hms.append('0')
                    one_data.append(int(hms[0])*10000+int(hms[1])*100+int(hms[2]))
                    one_data.append(float(strs[2]))
                    one_data.append(float(strs[3]))
                    one_data.append(float(strs[4]))
            if(len(one_data)>0):list.append(one_data)    
            line = file.readline()
        tL = bd.timelist_data(len(list),list)
        return tL
            

            