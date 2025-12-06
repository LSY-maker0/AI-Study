"""
example02 - 全局变量和局部变量

Python程序中搜索一个变量是按照LEGB顺序进行搜索的

Local(局部作用域) --> Embeded(嵌套作用域) --> Global(全局作用域) --> Built-in(内置作用域) --> name ... not defined

global - 声明使用全局变量，或将一个局部变量放到全局作用域
nonlocal - 声明使用嵌套作用域(上一级)的变量（不使用局部变量）

Author: lsy
Date: 2025/12/6
"""

x=100

def foo():
    # global x # 获取全局的x，改为200
    x=200

    def bar():
        # nonlocal x # 获取上一级x，改为300
        x=300

        def baz():
            nonlocal x
            x=400
            print(x)
        baz()
        print(x)

    bar()
    print(x)
foo()
print(x)