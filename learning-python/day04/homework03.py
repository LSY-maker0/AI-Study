"""
homework03 - 输入两个非负整数m和n（m>=n），计算C(m,n)的值
C(m,n)=m!/n!/(m-n)!

Author: lsy
Date: 2025/12/3
"""

# as --> alias --> 别名

# 从math模块导入factorial函数并别名为fac
from math import factorial as fac

m=int(input('m = '))
n=int(input('n = '))

# result=1
# for i in range(2,m+1):
#     result*=i
# for i in range(2,n+1):
#     result//=i
# for i in range(2,m-n+1):
#     result//=i
# print(result)

print(fac(m)//fac(n)//fac(m-n))