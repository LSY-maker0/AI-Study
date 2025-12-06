# 30个人报数报到9扔掉，15男15女，15女全活下来，求女位置

# nums=[True]*30

# counter,index,number=0,0,0

# while counter<15:
#   if nums[index]:
#     number+=1
#     if number==9:
#       nums[index]=False
#       counter+=1
#       number=0
#   index+=1
#   if index==30:
#     index=0

# print(nums)

# counter,index,number=0,0,0

# while counter<15:
#   if nums[index]:
#     number+=1
#     if number==9:
#       nums[index]=False
#       counter+=1
#       number=0
#   index+=1
#   if index==30:
#     index=0
# for num in nums:
#   # 三元运算符 if 后面为 True 取前面 Flase 取后面
#   print('女' if num else '男',end=(' '))


persons = [i for i in range(1, 31)]
for _ in range(15):
    persons = persons[9:] + persons[:8]
print(persons)
