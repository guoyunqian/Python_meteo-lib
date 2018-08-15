# coding: utf-8
import operator
#统计一个数列中出现次数最多的值
def majorityCount(dataList):
    classCount=valueCountDict(dataList)
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

#给定一个数列，以字典形式返回其中各个值出现的概率
def valuePDict(dataList):
    dataNum=len(dataList)
    valueP=valueCountDict(dataList)
    for key in valueP.keys():
        valueP[key]/=float(dataNum)
    return valueP

#给定一个数列，以字典形式返回其中各个值出现的频次
def valueCountDict(dataList):
    dat=dataList.copy()
    dat.sort()
    count={}
    for val in dat:
        if val not in count.keys():count[val]=0
        count[val]+=1
    return count
#给定一个数列，以列表形式返回其中各个值出现的频次
def valueCountList(dataList):
    count={}
    for val in dataList:
        if val not in count.keys():count[val]=0
        count[val]+=1
    sortedCount=sorted(count.items(),key=operator.itemgetter(0))
    return sortedCount