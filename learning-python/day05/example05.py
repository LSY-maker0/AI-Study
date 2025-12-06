"""
example05 - 

Author: lsy
Date: 2025/12/4
"""
import random

nums=[1,2,3,4,5]
# print(sum(nums),sum(nums)/len(nums),max(nums),min(nums))

mean_value=sum(nums)/len(nums)
total=0
for num in nums:
    total+=(num-mean_value)**2

# 方差 --> variance --> var --> cov（协方差）
var_value=total/(len(nums)-1)

# 标准差 --> standard deviation --> std / stdev
std_value=total**0.5

print(random.random())# 随机0到1的小数
print(random.randrange(1,101))# 随机0到1的小数