"""
__init__.py - 包的初始化文件

任务：写一个函数，传入一个文件名，返回这个文件的后缀名

hello.py -> py / .py
hello.txt -> txt / .txt
.abc -> 没有空字符串

suffix --> 后缀
prefix --> 前缀

Author: lsy
Date: 2025/12/7
"""
# import 该包就可以获取该函数
# print('使用自定义加法函数') # 只要使用该包就会执行

# 有*号时，前面的是位置参数，对号入座
# *后面的参数是命名关键字参数，调用函数传参时，必须写成"参数名=参数值"形式

def get_suffix(filename,*,has_hot:bool=False):
    position=filename.rfind('.')
    if position<=0:
        return ''
    if not has_hot:
        position+=1
    return filename[position:]

