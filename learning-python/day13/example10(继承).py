"""
example10(继承) -

继承：从已有的类进行扩展，创建出新的类，这个过程就叫继承
提供继承信息的类叫做父类（超类，基类），得到继承信息的类称为子类（派生类）

子类直接从父类继承公共的属性和行为，再添加自己特有的属性和行为，
所以子类一定是比父类更强大的，任何时候都可以用子类对象去替代父类对象

继承是实现代码复用过的一种手段，但是千万不要滥用继承

Author: lsy
Date: 2025/12/10
"""
class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def eat(self):
        print(f'{self.name} 吃')

    def play(self):
        print(f'{self.name} 玩')

class Computer:
    pass

class Vehicle:
    pass

class Student(Person):

    def __init__(self,name,age,grade):
        super().__init__(name,age)
        self.grade=grade
        self.computer=[Computer(),Computer()] # 关联关系 has-a

    def drive(self,vehicle):
        pass

    def study(self):
        print(f'{self.name} 在学习')


class Teacher(Person):
    def __init__(self,name,age,title):
        super().__init__(name,age)
        self.title=title

    def teach(self):
        print(f'{self.name}在教{self.title}')

def main():
    stu=Student('张三',18,'三年级')
    stu.eat()
    teacher=Teacher('李四',30,'语文')
    teacher.teach()

if __name__ == '__main__':
    main()

