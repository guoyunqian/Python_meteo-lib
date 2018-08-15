#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import pandas as pd

def sta_data(dframe,column_num):
        columns = [0, 1, column_num]
        return pd.DataFrame(dframe.ix[:,columns].values,dframe.index,columns = ['lon','lat','dat'])