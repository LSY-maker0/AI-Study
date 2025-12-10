"""
example11(两个类关系) - 两个类之间有哪些可能的关系？

～ is-a关系：继承 --> class Student(Person)
    a student is a person
    a teacher is a person
～ has-a关系：关联 --> 把一个类的对象当成另外一个类的对象的属性
    - (普通)关联
        a person has an identity card. 普通
        a car has an engine.    强关联
    - 强关联：整体和部分的关联，聚合和合成
～ use-a关系：依赖 --> 一个类的对象作为另一个类的方法的参数或返回值
    a person use a vehicle


多重继承（尽量减少），避免菱形继承

Author: lsy
Date: 2025/12/10
"""

# 唐僧有三个徒弟（关联），使用了马（依赖）

