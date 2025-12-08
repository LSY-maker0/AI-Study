"""
example05 - 定义描述三角形的类，提供计算周长和面积的方法

我们在类里面写的函数，通常称之为方法，它们基本上都是发送给对象的消息。
但是有的时候，我们的消息并不想发给对象，而是希望发给这个类（类本身也是一个对象）

静态方法 - 发给类的消息 --> @staticmethod --> 装饰器
类方法 - 发给类的消息 --> @classmethod --> 装饰器 -> 类方法的第一个参数（cls）是接收消息的类

Author: lsy
Date: 2025/12/8
"""


class Triangle:
    def __init__(self, a, b, c):
        if not Triangle.is_valid(a, b, c):
            raise ValueError('无效的边长，无法构成三角形')
        self.a = a
        self.b = b
        self.c = c

    # @classmethod
    # def is_valid(cls,a,b,c):
    #     return a + b > c and a + c > b and b + c > a

    @staticmethod
    def is_valid(a,b,c):
        return a + b > c and a + c > b and b + c > a

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        half = self.perimeter() / 2
        return (half * (half - self.a) * (half - self.b) * (half - self.c)) ** 0.5


if __name__ == '__main__':
    try:
        t = Triangle(1,2,1)
        print(t.perimeter())
        print(t.area())
    except ValueError as err:
        print(err)