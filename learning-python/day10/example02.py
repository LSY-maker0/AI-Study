dict1={
  'A':100,
  'B':200,
  'C':300
}

dict2={
  'D':100,
  'E':200,
  'F':300
}

dict1.update(dict2) # 更新dict1的值
print(dict1)

# 删除 不存在报错KeyError
del dict1['D']
dict1.popitem()
# dict1.pop['D']

# dict1.clear()

print(dict1.setdefault('C',800))
print(dict1.setdefault('A')) # 可返回对应的值
print(dict1.setdefault('O')) # None
print(dict1.setdefault('P',800))

print(dict1)
