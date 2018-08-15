#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-
import numpy as np
from copy import deepcopy
import basicdatas as bd
import os
import basicdatafunctions as bf
import math
from fileinput import filename
import zlib
import netCDF4 as nc

def write_to_micaps4(grd,filename = "a.txt",effectiveNum = 6):
    dir = os.path.split(os.path.abspath(filename))[0]
    if os.path.isdir(dir):
        br = open(filename,'w')
        vmax = np.max(grd.dat)
        vmin = np.min(grd.dat)
        if vmax - vmin < 1e-10 :
            vmax = vmin + 1.1 
        dif=(vmax - vmin) / 10.0
        inte=math.pow(10,math.floor(math.log10(dif)));
        #用基本间隔，将最大最小值除于间隔后小数点部分去除，最后把间隔也整数化
        r=dif/inte;
        if  r<3 and r>=1.5:
            inte = inte*2
        elif r<4.5 and r>=3 :
            inte = inte*4
        elif r<5.5 and r>=4.5:
            inte=inte*5
        elif r<7 and r>=5.5:
            inte=inte*6
        elif r>=7 :
            inte=inte*8   
        vmin = inte * ((int)(vmin / inte) - 1)
        vmax = inte * ((int)(vmax / inte) + 1)

        end = len(filename)
        start = max(0, end-16)
        str1=("diamond 4 " + filename[start:end] + "\n2018 01 01 08 0 9999\n"
            + str(grd.dlon) + " " + str(grd.dlat) + " " + str(grd.slon) + " " + str(grd.elon) + " "
            + str(grd.slat) + " " + str(grd.elat) + " " + str(grd.nlon) + " " + str(grd.nlat) + " "
            + str(inte) + " " + str(vmin) + " " + str(vmax) + " 1 0")
        try:
            br.write(str1);
            format_str = "%." + str(effectiveNum) +"f "
            for j in range(grd.nlat):
                br.write("\n");
                for i in range(grd.nlon):
                    br.write(format_str%grd.dat[j,i])
            br.close()
        except Exception as e:
            print(e.args)
            return 1
        return 0
    else:
        return 1

def write_to_nc(grd,filename = "a.txt",effectiveNum = None):
    dir = os.path.split(os.path.abspath(filename))[0]

    if os.path.isdir(dir):
        lonS = np.linspace(grd.slon, grd.elon, grd.nlon)
        latS = np.linspace(grd.slat, grd.elat, grd.nlat)
        da = nc.Dataset(filename, 'w', format='NETCDF4')
        da.createDimension('lons', grd.nlon)  # 创建坐标点
        da.createDimension('lats', grd.nlat)  # 创建坐标点
        da.createVariable("lon",'f',("lons"))  #添加coordinates  'f'为数据类型，不可或缺
        da.createVariable("lat",'f',("lats"))  #添加coordinates  'f'为数据类型，不可或缺
        da.variables['lat'][:]=latS     #填充数据
        da.variables['lon'][:]=lonS     #填充数据
        if(not effectiveNum is None):
            da.createVariable('value', 'f4', ('lons', 'lats'),zlib=True,least_significant_digit=effectiveNum)  # 创建变量，shape=(627,652)  'f'为数据类型，不可或缺
        else:
            da.createVariable('value', 'f4', ('lons', 'lats'), zlib=True)
        da.variables['value'][:] = grd.dat.T  # 填充数据
        da.close()
        return 0
    else:
        return 1



def write_to_compressed(grd,filename = "a.txt",grade_num = 1000,continuous = True,accuracy = None):


    dir = os.path.split(os.path.abspath(filename))[0]
    if os.path.isdir(dir):
        vmax = grd.dat.max()
        vmin = grd.dat.min()
        if accuracy is not None :
            grade_num = int((vmax - vmin) / accuracy)
        if(vmax == vmin):
            head1_bytes = np.ndarray.tobytes(np.array([grd.slon, grd.elon, grd.slat, grd.elat, vmax, vmin], dtype=np.float32))
            head2_bytes = np.ndarray.tobytes(np.array([grd.nlon,grd.nlat,0,0],dtype= np.uint16))
            all_bytes = head1_bytes + head2_bytes
            data_bytes_compressed = zlib.compress(all_bytes)
            br = open(filename, 'wb')
            br.write(data_bytes_compressed)
            br.close()
        elif(continuous):
            nlon_1 = grd.nlon - 1
            nlat_1 = grd.nlat - 1
            sparse_rate = 1
            grade_int = np.rint((grd.dat - vmin) * grade_num / (vmax - vmin))
            bins = '1000000000000000'
            k = 15
            while nlon_1 % 2 == 0 and nlat_1 % 2 ==0 and nlon_1 > 1 and nlat_1 > 1 and sparse_rate <128:
                nlon_1 /= 2
                nlat_1 /= 2
                sparse_rate *= 2
                k -= 2
            bins = bins[:k] + '1' +bins[k+1:]
            most_sparsed_grade = grade_int[::sparse_rate,::sparse_rate]
            if (grade_num <= 255):
                most_sparsed_grade = most_sparsed_grade.astype(np.uint8)
                bins = '0'+ bins[1:]
            else:
                most_sparsed_grade = most_sparsed_grade.astype(np.uint16)
            most_sparsed_grade_bytes = np.ndarray.tobytes(most_sparsed_grade)
            dgrade_bytes = []
            while sparse_rate > 1:
                grd_int_0 = bf.grid_data(bf.grid(grd.slon,grd.dlon*sparse_rate,grd.elon,grd.slat,grd.dlat*sparse_rate,grd.elat))
                grd_int_0.dat[:,:] = grade_int[::sparse_rate,::sparse_rate]
                sparse_rate = int(sparse_rate / 2)
                grd_int_1 = bf.ggf.cubicInterpolation(grd_int_0,bf.grid(grd.slon,grd.dlon*sparse_rate,grd.elon,grd.slat,grd.dlat*sparse_rate,grd.elat))
                d_int = np.rint(grd_int_1.dat) - grade_int[::sparse_rate,::sparse_rate]
                d_int_odd = d_int[::2,1::2]
                max_dgrade = d_int_odd.max()
                min_dgrade = d_int_odd.min()
                k += 1
                if(max_dgrade <128 and min_dgrade >= -128):
                    dgrade_bytes.append(np.ndarray.tobytes(d_int_odd.astype(np.int8)))
                else:
                    dgrade_bytes.append(np.ndarray.tobytes(d_int_odd.astype(np.int16)))
                    bins = bins[:k] + '1' + bins[k + 1:]
                d_int_even = d_int[1::2,:]
                max_dgrade = d_int_even.max()
                min_dgrade = d_int_even.min()
                k += 1
                if (max_dgrade < 128 and min_dgrade >= -128):
                    dgrade_bytes.append(np.ndarray.tobytes(d_int_even.astype(np.int8)))
                else:
                    dgrade_bytes.append(np.ndarray.tobytes(d_int_even.astype(np.int16)))
                    bins = bins[:k] + '1' + bins[k + 1:]
            uint_8_or_16 = int('0b'+bins, 2) # + int(math.pow(2,15))
            head1_bytes = np.ndarray.tobytes(np.array([grd.slon, grd.elon, grd.slat, grd.elat, vmax, vmin], dtype=np.float32))
            head2_bytes = np.ndarray.tobytes(np.array([grd.nlon,grd.nlat,grade_num,uint_8_or_16],dtype= np.uint16))
            all_bytes = head1_bytes + head2_bytes + most_sparsed_grade_bytes
            for b in dgrade_bytes:
                all_bytes = all_bytes + b
            bytes_compressed = zlib.compress(all_bytes)
            br = open(filename, 'wb')
            br.write(bytes_compressed)
            br.close()
            #print(len(bytes_compressed)/(grd.nlon * grd.nlat))
        else:
            if (grade_num <= 255):
                grd_int = np.rint((grade_num * (grd.dat - vmin) / (vmax - vmin))).astype(np.uint8)
                uint_8_or_16 = int('0b0000000000000001', 2)
            else:
                grd_int = np.rint((grade_num * (grd.dat - vmin) / (vmax - vmin))).astype(np.uint16)
                uint_8_or_16 = int('0b1000000000000001', 2)
            dat_bytes = np.ndarray.tobytes(grd_int)
            head1_bytes = np.ndarray.tobytes(np.array([grd.slon, grd.elon, grd.slat, grd.elat, vmax, vmin], dtype=np.float32))
            head2_bytes = np.ndarray.tobytes(np.array([grd.nlon,grd.nlat,grade_num,uint_8_or_16],dtype= np.uint16))
            all_bytes = head1_bytes + head2_bytes + dat_bytes
            data_bytes_compressed = zlib.compress(all_bytes)
            br = open(filename, 'wb')
            br.write(data_bytes_compressed)
            br.close()
            #print(len(data_bytes_compressed) / (grd.nlon * grd.nlat))
    return
