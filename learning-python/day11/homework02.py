"""
homework02 - 设计获取样本数据描述性统计信息的函数

集中趋势：均值，中位数，众数
离散趋势：极差，方差，标准差

Author: lsy
Date: 2025/12/6
"""
import math

def ptp(data):
    """极差"""
    return max(data) - min(data)

def average(data):
    """均值"""
    return sum(data) / len(data)

def variance(data):
    """方差"""
    x_bar=average(data)
    total=0
    for x in data:
        total+=(x-x_bar)**2
    return total/(len(data)-1)

def standard_deviation(data):
    """标准差"""
    return math.sqrt(variance(data))

def median(data):
    temp,size = sorted(data),len(data)
    if size % 2 != 0:
        return temp[size//2]
    else:
        return average(temp[size//2-1:size//2+1])

nums=[1,2,3,9,8,6,4]
print(ptp(nums))
print(standard_deviation(nums))
print(median(nums))
