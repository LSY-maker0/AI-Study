"""
example02(一等函数的概念) - 一等函数（高阶函数）

Python中的函数是一等函数：
1. 函数可以作为参数，
2. 可以作为函数的返回值
3. 函数可以赋值给变量

如果把函数作为函数的参数或者返回值，这种玩法统称之为高阶函数。
通常使用高阶函数可以实现对原来函数的解耦操作

Author: lsy
Date: 2025/12/7
"""
import operator

# def mul(*args):
#     total = 1
#     for arg in args:
#         total *= arg
#     return total
#
#
# def add(*args):
#     total = 0
#     for arg in args:
#         total += arg
#     return total


# fn --> 一个实现二元运算的函数(可以做任意的二元运算)
def calc(*args,op,init_value, **kwargs):
    total = init_value
    for arg in args:
        if type(arg) in (int, float):
            total = op(total, arg)
    for value in kwargs.values():
        if type(value) in (int, float):
            total = op(total, value)
    return total


def add(a,b):
    return a + b

def mul(a,b):
    return a * b

def sub(a,b):
    return a - b

print(calc(1,2,3,4,op=operator.add,init_value=0))
print(calc(1,2,3,4,op=mul,init_value=1))
print(calc(1,2,3,4,op=sub,init_value=100))