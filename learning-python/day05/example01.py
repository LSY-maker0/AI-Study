"""
example01 - 容器型数据类型（用一个变量可以保存多个数据）

～ 列表（list）-
～ 元组（tuple）-
～ 集合（set）-
～ 字典（dict）-

Author: lsy
Date: 2025/12/4
"""

nums = [1,5,3,4,2,2]
print(nums.append(2))
nums.insert(0,100)
nums.pop()
nums.remove(100)
nums.sort()
print(nums)
print(type(nums))
