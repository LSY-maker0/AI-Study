"""
example03 - 列表的遍历

Author: lsy
Date: 2025/12/4
"""

nums=[12,22,32,42,52]
# nums[0]=1
# for i in range(len(nums)):
#     print(nums[i])
# print(f'负向索引-2值为: {nums[-2]}')

# for num in nums: # 无法更改原列表的值
#     print(num)

# 先通过enumerate函数对列表进行预处理
# 循环遍历的时候既可以获取到索引（下标）又可以获取到元素
for i,num in enumerate(nums):
    print(i,num)