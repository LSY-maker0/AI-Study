"""
homework05 - 输入三角形三条边的长度，如果能构成三角形就计算周长和面积，如果不能构成三角形
提示用户重新输入，直到正确

任意两边大于第三边

Author: lsy
Date: 2025/12/3
"""

while True:
    a = float(input('a= '))
    b = float(input('b= '))
    c = float(input('c= '))
    if a + b > c and a + c > b and b + c > a:
        perimeter = a + b + c
        half = perimeter / 2
        # 海伦公式
        # sqrt 平方根
        area = (half * (half - a) * (half - b) * (half - c)) ** 0.5
        print(f'perimeter = {perimeter}, area = {area}')
        break
    else:
        print('请重新输入')
