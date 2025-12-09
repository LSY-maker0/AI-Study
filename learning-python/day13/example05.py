"""
example05 - 定义描述三角形的类，提供计算周长和面积的方法

我们在类里面写的函数，通常称之为方法，它们基本上都是发送给对象的消息。
但是有的时候，我们的消息并不想发给对象，而是希望发给这个类（类本身也是一个对象）

静态方法 - 发给类的消息 --> @staticmethod --> 装饰器
类方法 - 发给类的消息 --> @classmethod --> 装饰器 -> 类方法的第一个参数（cls）是接收消息的类

Author: lsy
Date: 2025/12/8
"""


# 构造器创建的对象基本都在堆空间（有些字符串放常量池），而对象的引用通常是放在栈上的，通过对象引用（变量）
# 就可以访问到对象并向其发出消息

# 如果对象没有被引用，那么Python解释器的自动内存管理机制会对其空间进行回收

# 魔术方法：有特殊用途的方法
# __init__ 初始化方法，创建对象时候自动调用
# __str__ 获得对象的字符串表示，调用print函数输出对象会被自动调用
# __repr__ 获得对象的字符串表示，把对象放到容器中，print输出时自动调用
#     representation

class Triangle:
    def __init__(self, a, b, c):
        if not Triangle.is_valid(a, b, c):
            raise ValueError('无效的边长，无法构成三角形')
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return self.show()

    # def __repr__(self): # 放在容器中print自动调用
    #     return self.show()

    def show(self):
        return f'边长分别为{self.a},{self.b},{self.c}'

    # @classmethod
    # def is_valid(cls,a,b,c):
    #     return a + b > c and a + c > b and b + c > a

    @staticmethod
    def is_valid(a, b, c):
        return a + b > c and a + c > b and b + c > a

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        half = self.perimeter() / 2
        return (half * (half - self.a) * (half - self.b) * (half - self.c)) ** 0.5

def main():
    try:
        t = Triangle(3, 4, 5)
        print(t)
        print(t.perimeter())
        print(t.area())

        list=[t]
        print(list)
    except ValueError as err:
        print(err)

if __name__ == '__main__':
    main()
