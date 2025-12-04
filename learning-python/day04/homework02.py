"""
homework02 - 找出1-10000之间的完美数（除自身外所有因子的和等于这个数）

6 = 1 + 2 + 3
28 = 1 + 2 + 4 + 7 + 14

Author: lsy
Date: 2025/12/3
"""
import time

start = time.time()
for num in range(1,100000):
    current=1
    for i in range(2,int(num**0.5)+1):
        if num % i == 0:
            current+=i
            if num//i!=i:
                current += num // i

    if current==num:
        print(num)

end = time.time()
print(f'执行了{end-start}秒')
