"""
example10 - 求 x 到 y 的最大公约数

bug ---> 缺陷/故障/问题 ---> debug(调试)
encode（编码）/decode （解码）

Author: lsy
Date: 2025/12/3
"""


# 15 27
x = int(input('x = '))
y = int(input('y = '))
# for i in range(x, 0,-1):
#     if x%i==0 and y%i==0:
#         print(i)
#         break
while y % x != 0:
    # temp=y
    # y=x
    # x=temp%y
    x, y = y % x, x
print(x)
