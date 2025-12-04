"""
example07 - 求 1-100 之前 3 或 5 的倍数的和

Author: lsy
Date: 2025/12/3
"""

total=0
for i in range(1, 101):
    if i%3==0 or i%5==0:
        total+=i
    else:
        pass
print(total)
