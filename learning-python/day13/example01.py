"""
example01 - 面向对象编程

指令式编程 --> 面向对象（函数）编程 --> 程序比较简单的时候

编程范式（程序设计的方法论）：面向对象编程 / 函数式编程

对象：对象是可以接收消息的实体，面向对象编程就是通过给对象发消息达到解决问题的目标。

对象 = 数据 + 函数（方法） --> 对象将数据和操作数据的函数逻辑上变成了一个整体

类：将有共同特征（静态特征和动态特征）的对象的共同特征抽取出来之后得到的一个抽象概念

简单地说，类是对象的蓝图（模版），有了类才能够创建出这种对象

面向对象编程
1. 定义类 --> 类的命名使用驼峰命名
    - 数据抽象：找到和对象相关的静态特征（属性）
    - 行为抽象：找到和对象相关的动态特征（方法）
2. 造对象
3. 发消息

Author: lsy
Date: 2025/12/8
"""

class Student:
    """学生"""
    # __slots__ = ("name", "age") # 只能有这两个属性

    # 数据抽象
    def __init__(self,name,age):
        self.name = name # 变成私有属性，无法更改
        self.age = age

    # def __str__(self):
    #     return f'{self.name} {self.age}'
    #
    # def __repr__(self):
    #     return f'{self.name} {self.age}'

    # 行为抽象(方法)
    def eat(self):
        """吃饭"""
        print(f'{self.name}正在吃饭')

    def study(self,course_name):
        """学习"""
        print(f'{self.name}在学习{course_name}课程')

    def play(self,game_name):
        """玩"""
        print(f'{self.name}正在玩{game_name}')

def main():
    stu=Student('张三',18)

if __name__ == '__main__':
    main()