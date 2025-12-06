"""
example02 - 

Author: lsy
Date: 2025/12/4
"""

import random

fs=[0,0,0,0,0,0]
# fs = [0] * 6
# print(fs)

for _ in range(60000):
    face = random.randrange(1,7)
    fs[face-1]+=1
for i,value in enumerate(fs):
    print(f'{i+1}点摇出了{value}次')