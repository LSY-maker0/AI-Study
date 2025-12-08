"""
foo - 解决命名冲突

方法一：取别名解决命名冲突
方法二：完全限定名

Author: lsy
Date: 2025/12/7
"""

# 方法一：取别名解决命名冲突
# from utils.add import add as add1
# from demo.example01 import add as add2

# 方法二：完全限定名
# import utils.add
import demo.example01

from utils import add
from demo import example01

add.add(1,4)
example01.add(1,4)

