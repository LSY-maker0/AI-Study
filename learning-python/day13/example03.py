"""
example03 - 用面向对象编程解决实际问题

Author: lsy
Date: 2025/12/8
"""
import math

class Circle:

    def __init__(self, radius):
        self.radius = radius

    def perimeter(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * self.radius ** 2

if __name__ == '__main__':
    r=float(input('请输入游泳池的半径：'))
    c1,c2=Circle(r),Circle(r+3)

    fence_price=c2.perimeter()*38.5 # 围墙
    aisle_price=(c2.area()-c1.area())*58.5 # 过道
