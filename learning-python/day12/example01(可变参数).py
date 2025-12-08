"""
example01 - 在设计函数时候，函数的参数个数暂时无法确定

位置参数 --> positional argument
关键字参数 --> keyword argument --> 参数名=参数值

关键字参数一定在位置参数后面

Author: lsy
Date: 2025/12/7
"""

# *args --> 可变参数 --> 可以接收零个或任意多个位置参数（打包成元组）
# **kwargs --> 可以接受零个或任意多个关键字参数（打包成字典）
def add(*args,**kwargs):
    # return sum(a)
    # print(a) # 元组
    # print(kwargs)

    total = 0
    for arg in args:
        if type(arg) in (int, float):
            total += arg

    for value in kwargs.values():
        if type(value) in (int, float):
            total += value

    return total

print(add(1, 2, 3,a=1,b=2,c='hello'))
