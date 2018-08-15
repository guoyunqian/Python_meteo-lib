#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy

class timelist_data:
    def __init__(self,nt,list = []):
        self.num = nt
        if(len(list)>0 and len(list[0])==5):
            self.dat = np.array(list)
        else:
            self.dat = np.zeros([nt,5])
        
    def tostring(self):
        str1 = "timelist data size: " + str(self.num) + "\n"
        str2 = str(self.dat)
        return str1 + str2

    def copy(self):
        return deepcopy(self)