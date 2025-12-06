items=[1,2,3,4,1,1,3,4,5,67,2,2]

# 去重
unique_items=[]

for item in items:
  # if unique_items.count(item)==0:
  if item not in unique_items:
    unique_items.append(item)
print(unique_items)

# 找出列表中最多的元素
num,max_counter=[items[0]],items.count(items[0])

# for item in items[1:]:
#   if items.count(item)>max_counter:
#     # num=item
#     # max_counter=items.count(item)
#     num,max_counter=item,items.count(item)
# print(num)

for item in items[1:]:
  curr_counter=items.count(item)
  if curr_counter>max_counter:
    num.clear
    num.append(item)
    max_counter=curr_counter
  elif curr_counter==max_counter:
    if item not in num:
      num.append(item)

print(num)