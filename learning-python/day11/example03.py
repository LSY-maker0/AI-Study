"""
example03 - 定义和使用函数

计算组合数 C(M,N) = M! / N! / (M-N)! (M>=N)

使用函数的时候，要么是Python标准库中或三方库
或者是自己写

Author: lsy
Date: 2025/12/6
"""

from math import factorial as f

def fac(m):
    """
    求阶乘
    :param m:
    :return:
    """
    num=1
    for i in range(2,m+1):
        num*=i
    return num

def C(m,n):
    return fac(m)//fac(n)//fac(m-n)

m=int(input('输入m:'))
n=int(input('输入n:'))
print(C(m,n))