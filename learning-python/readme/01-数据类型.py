"""
readme.py - 01- 数据类型及其方法

Author: lsy
Date: 2025/12/6
"""
from pyexpat.errors import messages

"""
Python数据类型
1. 基本数据类型：int,float,bool,str,NoneType(空值：None)
2. 容器数据类型：list(列表),set(集合),dict(字典)，tuple(元组，不可变)
"""

"""
== 和 is
== 比较的是值，is 比较的是内存([-2,256]共用一个内存)
直接赋值时，编译器的优化机制会使得共用同一地址
当后面输入时，只有-2到256的输入相同的值返回True，其他为False（动态分配内存）
"""
# a=200
# b=int(input('输入')) # 输入200为True
# print(a is b)
#
# c=257
# d=int(input('输入')) # 输入257为False
# print(c is d) # False

"-------------------1. 基本数据类型------------------------"
"""
1. 基本数据类型

a=12
print(a)
print(type(1))    # <class 'int'>
print(type(1.23)) # <class 'float'>
print(type(True)) # <class 'bool'>
print(type('a'))  # <class 'str'>
print(type(None)) # <class 'NoneType'>
"""

"-------------------2. 列表------------------------"
"""
2. 列表 --> (nums=[1,'a','b'])
列表遍历 for i in nums 或 for index,num in enumerate(nums)
列表上的方法：
获取：len(),sum(),count(),max(),min(),index(),find(),sort()
修改：append,pop(),clear(),insert(index,num),remove(index,num-从index开始去除num值)
"""
# 1 字面量
nums1=[1,'abc',2,3,4,5]
# 2 生成式
nums2=[i for i in range(1,6)]

# 遍历
# for i in nums1:
#     print(i)
# for index,num in enumerate(nums1):
#     print(index,num)

# print(nums1[1:])
# print(nums1[1:3])
# print(nums1[:3])

# a,*b,c=1,2,3,4,5,6
# print(b) # 中间全部打包给b

"-------------------3. 元组------------------------"
"""
3. 元组（tuple） --> nums=(1,'a','b'),不能被修改，可以重新赋值
性能优化，tuple内存固定，创建和访问速度快，访问时间复杂度为O(1),占用内存小
hash存储
"""
nums=(1,2,'abc')
# for num in nums:
#     print(num)

"-------------------4. 字符串------------------------"
"""
4. 字符串上的方法 --> （a='hello world'） a:97 A:65
- 1. 转大小写：a.upper(),lower(),capitalize()首字母大写,title()每个单词（.,分割）首字母大写
- 2. 相关属性：a.isdigit(),isalpha(),isalnum()英文+数字，isascii() ascii中的字符（无中文，英文数字符合）
- 3. 查找：a.index('a',123)-rindex,lindex,找不到默认123（没设置报错）
    a.find()找不到返回-1-lfind,rfind
- 4. 左右填充：a.center(20,'~'),ljust(),rjust()，a.zfiff(20)->左边0填充(zerofill)
    'hello' in a 判断是否在字符串里面
- 5. 格式化输出
    print('%d+%d=%.2f' % (1,2,1+2)) # 保留两位小数点
    print('{}+{}={}'.format(1,2,1+2))
    print('{2}+{1}={0}'.format(1+2,1,2))
    a,b=1,2
    最推荐 --> print(f'{a}+{b}={a+b}')
    
    字符串替换：a.replace('world','newWorld')
    strip()去除两遍的空格 lstrip(),rstrip()
- 6. 字符串的拆分和合并 a.split(',') '#'.join(list)
- 7. 编码，一种字符集换另一种 str -> encode -> bytes(decode)
    a='我是谁'
    b=a.encode('utf-8') # b'\xe6\x88\x91\xe6\x98\xaf\xe8\xb0\x81'
    c=b.decode('utf-8') # 我是谁
- 8. 凯撒密码 table=str.maketrans('ab','cd') message.translate(table)
    messages='ab,ab'
    table=str.maketrans('ab','cd')
    print(messages.translate(table)) # cd,cd
- 9. 随机取值 
    import string
    print(string.digits) # 0123456789
    print(string.ascii_letters) # abc...
    
    import random
    a='fhoia'
    print(random.sample([1,2,3,4,5,6,7,8,9],3)) # 不放回抽样
    print(random.choices('afai',k=2)) # ['a'] 放回抽样（默认抽一个，加的话一定要加k）
    print(random.choice('sda')) # 抽一个
"""
# a=1
# # 格式化输出
# a='\t hello world\t' # \ 为转义字符
# print(r'a为{a}') # 原始字符串输出
# print(f'a为{a}') # 格式化字符串输出

"-------------------5. 集合------------------------"
"""
5. 集合 set={1,2,3} （无序性，互异性，确定性）
- 1. 定义
set1={1,2,3}
set2=set([1,2,3]) # set函数接收一个可迭代的对象
print(set1)
print(set2)

# 交(&)并(|)差(-)，对称差(^)
不能存列表，因为其可变，无法使用哈希存储

- 2. 方法
set.add(1)
set.discard(1)
set.pop() # 随机删除
set.clear() # 清空
frozenset(set1) # 不可变集合 可以用作dict字典的key
"""

"-------------------6. 字典------------------------"
"""
6. 字典（dict）
"""
student={
    'name':'张三',
    'age':18,
    'score':80,
}
print(student.get('name','查不到默认返回我')) # 如果没有该属性返回 None

# 键值对反过来
# zip就是将两个可迭代对象一对一打包起来
print(dict(zip(student.values(),student.keys())))

stocks={
    'a':120,
    'b':22,
    'c':34,
    'd':55,
}

# 排序
print(sorted(stocks,key=stocks.get,reverse=True))

# 统计单词出现过的次数
words='hfiuahhadsafla'
counter_dict={}
for word in words:
    counter_dict[word]=counter_dict.get(word,0)+1 # 体会
print(counter_dict)








