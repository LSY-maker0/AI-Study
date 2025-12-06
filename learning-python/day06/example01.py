items = ['a', 'b', 'c', 'd', 'D', 'd', 'app']

# 添加元素
items.insert(1,'p')
print(items)

# 删除元素
items.pop(2) # 去除下标
items.remove('c') # 删除第一次出现的
print(items)

# 清空列表元素
# items.clear()
# print(items)

# print(items.index('d')) # 找到该元素返回对应的下标

if 'd' in items[3:]: # 如果3下表以后存在该值
  print(items.index('d',3)) # 从第3下标开始找

print(items.count('d')) # 统计元素在列表中出现了多少次