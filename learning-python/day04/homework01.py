"""
homework01 - 找出100到999之间的水仙花树（各位数字的立方和刚好等于这个数本身）

153 = 1^3 + 5^3 + 3^3

1234 -> 4321

Author: lsy
Date: 2025/12/3
"""

# for num in range(100,1000):
#     bw=num // 100
#     sw=num//10%10
#     gw=num % 10
#     if bw**3 + sw**3 + gw**3 == num:
#         print(num)

num=int(input('num = '))
result=0
while num>0:
    result=result*10+num%10
    num=num//10
print(result)




