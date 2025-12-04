"""
10 - 判断是否是闰年
四年一闰 百年不闰 四百年又闰

Author: lsy
Date: 2025/12/3
"""

a = int(input('a = '))
print(a % 4 == 0 and a % 100 != 0 or a % 400 == 0)
