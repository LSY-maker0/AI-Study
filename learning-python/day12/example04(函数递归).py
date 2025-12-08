"""
example04(函数递归) - 函数可以自己调用自己吗？

递归调用
无休止的调用，会将栈空间消耗殆尽，导致程序崩溃
栈空间小（512k，1M），很小部分属于栈空间

官方CPython默认情况下，调用栈的大小是1000次
import sys
sys.setrecursionlimit(10000) 改变默认栈调用次数

保存现场 --> 调用函数 --> 恢复现场
每个函数都有属于自己的栈结构，保存现场就是将整个栈结构保存起来
进出栈与js类似，入栈出栈

foo --> fuck up
bar --> beyond all recognization(认知)

Author: lsy
Date: 2025/12/7
"""

# def foo():
#     print("foo")
#
# def bar():
#     foo()
#     print("bar")
#
# def main():
#     bar()
#     print('Game Over')

# 递归函数
# 1. 递归公式
# 2. 截止条件
def fac(n):
    if n == 0:
        return 1
    return n * fac(n - 1)

if __name__ == '__main__':
    print(fac(3))

