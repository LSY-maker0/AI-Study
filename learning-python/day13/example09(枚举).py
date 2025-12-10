"""
example09 - 枚举

Python 中没有定义枚举类型的语法，但是可以通过继承Enum类来实现枚举类型
结论1:枚举类型时定义符合常量的最佳选择!!!
结论2:符号常量（有意义的名字）总是优于字面常量!!!

Author: lsy
Date: 2025/12/10
"""
from enum import Enum

class Suite(Enum):
    SPADE,HEART,CLUB,DIAMOND=range(4)

for suite in Suite:
    print(suite,suite.value)