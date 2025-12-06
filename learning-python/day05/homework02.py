"""
homework02 - 输入10个1-99的整数，计算平均值，找出最大值和最小值

Author: lsy
Date: 2025/12/4
"""

total=0
min_value,max_value=100,0
for _ in range(5):
    temp=int(input('请输入'))
    total+=temp
    if temp<min_value:
        min_value=temp
    if temp>max_value:
        max_value=temp
print(f'平均值：{total/10},最大值：{max_value},最小值：{min_value}')