# 排序算法
import random

nums = [1, 4, 3, 3, 5, 5, 6, 6, 0, 1]
# sorted_nums=[]


# while len(nums):
#   min_value=min(nums)
#   sorted_nums.append(min_value)
#   nums.remove(min_value)
# print(sorted_nums)

# 简单选择排序
# for i in range(0,len(nums)):
#   min_value,min_index=nums[i],i

#   for j in range(i,len(nums)):
#     if nums[j]<min_value:
#       min_index=j
#       min_value=nums[j]
#   if min_index!=i:
#     nums[i],nums[min_index]=nums[min_index],nums[i]

# print(nums)

# 冒泡
# 元素两两比较，把大的慢慢往上冒
# for i in range(len(nums)):
#   flag=True
#   for j in range(i,len(nums)):
#     if nums[i]>nums[j]:
#       nums[i],nums[j]=nums[j],nums[i]
#       flag=False
#   if flag:
#     break
# print(nums)

print(random.sample(nums, 5))  # 不放回抽样

print(random.choices(nums, k=5))  # 有放回抽样

print(random.choice(nums))  # 有放回抽样

random.shuffle(nums)
print(nums)
