"""
homework04 - 

Author: lsy
Date: 2025/12/4
"""

import random

# 列表的生成式语法（推导式）
# nums = [random.randrange(1,100) for _ in range(10)]
nums = [i for i in range(1,101,2)]
print(nums)
