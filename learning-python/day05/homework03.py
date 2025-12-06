"""
homework03 - 找出列表中第二大的值

Author: lsy
Date: 2025/12/4
"""

nums=[1,2,3,4,5,6,7,7]
m1,m2=nums[0],nums[1]

if m1>m2:
    m1,m2=m2,m1

for i in range(2,len(nums)):
    if nums[i]>m2:
        m1,m2=m2,nums[i]
    # elif nums[i]==m2:
    #     pass
    elif nums[i]>m1:
        m1=nums[i]
print(m1,m2)