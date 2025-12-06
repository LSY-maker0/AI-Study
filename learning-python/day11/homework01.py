"""
homework01 - 写一个函数随机生成验证码（数字和英文组成）

Author: lsy
Date: 2025/12/6
"""
import string
import random


# print(string.ascii_letters)
# print(string.digits)

def get_captcha_code(length: int = 4) -> str:
    """
    随机生成验证码
    :param length: 验证码长度
    :return: 随机验证码字符串
    """
    str = ''
    list = string.ascii_letters + string.digits
    for _ in range(length):
        str += random.choice(list)
    return str


print(get_captcha_code())


# 写程序的终极原则 单一职责（只做一件事） 高类聚，低耦合

def gcd(x: int, y: int) -> int:
    """最大公约数  例如 12 60
    :param x:
    :param y:
    :return:
    """
    while y % x != 0:
        x, y = y % x, x
    return x

def lcm(x: int, y: int) -> int:
    """最小公倍数

    :param x:
    :param y:
    :return:
    """

    return x*y // gcd(x, y)