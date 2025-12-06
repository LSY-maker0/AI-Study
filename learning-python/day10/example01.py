# 字典 --> 键值对
# 他的key为不可变数据类型

# 1.字面量语法
student={
  'id':'1001',
  'name':'张三',
  'age':14,
  'contacts':{
    'qq':'123',
    'wx':'12345',
  },
  1:'数字key',
  (1,2):'123123'
}

# for key in student:
#   print(key)

# print(student['id'])

# # 构造器函数
student2=dict(id=1002,name='李四')

# stu={} # 空字典
# stu1=set({}) # 空集合

# 生成式语法
# list1=[i for i in range(1,10)]
# print(list1)
# set1={i for i in range(1,10)}



dict={
  'name':'张三',
  'age':18,
  'contacts':{
    'qq':'123',
    'wx':'12345',
  },
}

# 长度
print(len(dict))

# 遍历键
for key in dict.keys():
  print(key)

# 遍历值
for value in dict.values():
  print(value)

# 成员运算，判断在不在字典里面
print('name' in dict) # True

# 索引运算，索引对应的值存在更改值，不存在增加一组"键值对"
dict['name']='改了名字'
print(dict)

# print(dict['dhaiuo'])
print(dict.get('name1','无名氏')) # None
# del dict['name'] # 删除某个key
# print(dict['name'])

if 'name' in dict:
  print(dict['name'])
 