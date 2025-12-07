"""
example04 - 获取A和B班成绩信息

如果使用其他模块（文件）通过import导入模块
直接导入函数 from homework02 import average

如果项目中的代码文件非常多，我们可以使用"包"（package）来管理模块，再通过模块来管理函数
包就是一个文件夹，而模块就是一个Python文件，通过这种方式就可以解决大型项目团队开发中经常遇到的命名冲突

Python中的from，import，as就是用来处理包和模块导入的操作的

Author: lsy
Date: 2025/12/7
"""

import random
import homework02
from homework02 import average # 可以使用as 别名

class_a_scores=[random.randrange(1,101) for _ in range(50)]
class_b_scores=[random.randrange(1,101) for _ in range(50)]

print(f'A班考试的平均分{average(class_a_scores)}')
print(f'中位数{homework02.median(class_b_scores)}')

from utils.add import add as addNum
print(addNum(1,2))
