"""
homework01 - 猜数字游戏

Author: lsy
Date: 2025/12/4
"""
# import math
# print(math.log2(4))

import random

num=random.randrange(1,101)
print(num)

flag=False

for _ in range(7):
    guess_num=int(input('请输入数字：'))
    if guess_num>num:
        print('猜大了')
    elif guess_num<num:
        print('猜小了')
    else:
        print('恭喜你猜对了')
        flag=True
        break

if not flag:
    print('智商余额显示不足')