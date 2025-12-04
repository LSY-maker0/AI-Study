"""
homework04 - 输入一个整数，判断它是不是质数（只能被1和自身整除的数）

Author: lsy
Date: 2025/12/3
"""
import math

# num= int(input('请输入一个正整数:'))
#
# flag=True
# for i in range(2,num):
#     if num%i==0:
#         flag = False
#         break
# if num>1 and flag:
#     print(f'{num}是质数')
# else:
#     print(f'{num}不是质数')

# print(math.sqrt(4))

# num=int(input('输入：'))

for i in range(1,10):
    for j in range(1,i+1):
        print(f'{j}*{i}={i*j}',end='\t')
    print()
