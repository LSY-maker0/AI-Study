"""
example03(Lambda函数) - 一句话就可以实现的函数

Lambda函数； op=lambda x, y: x + y

Author: lsy
Date: 2025/12/7
"""


def calc(*args, op, init_value, **kwargs):
    total = init_value
    for arg in args:
        if type(arg) in (int, float):
            total = op(total, arg)
    for value in kwargs.values():
        if type(value) in (int, float):
            total = op(total, value)
    return total


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def sub(a, b):
    return a - b


print(calc(1, 2, 3, 4, op=lambda x, y: x + y, init_value=0))
print(calc(1, 2, 3, 4, op=lambda x, y: x * y, init_value=1))