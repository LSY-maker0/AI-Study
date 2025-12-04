"""
homework01 - 输入圆的半径，计算圆的周长和面积

Author: lsy
Date: 2025/12/3
"""
import math # 导入

# print("Hello World!")
radius = float(input('请输入圆的半径: '))
perimeter = 2 * (math.pi * radius)
area = math.pi * radius ** 2
print(f'圆的周长是{perimeter:.2f}，面积是{area:.2f}')

# 可以回退任一版本