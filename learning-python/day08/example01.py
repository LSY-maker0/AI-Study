# 字符串概述

# a= 'hello ' \
# 'world'
# b="\'da\td\'sa"
# c='''
# hello

# world'''
# # '''相当于一个空行

# print(a)
# print(b)
# print(c)

# d='\\time up \\now'
d='c\\Users\\Adminstrator\\abc\\hello.py'
e='c/Users/Adminstrator/abc/hello.py'

# 原始字符串（没有转义字符）
f=r'c\Users\A"d"minstrator\abc\hello.py'

# 带占位符的字符串（格式化字符串）
g=f'文件路径：{d}'

# print(d)
print(e)
print(f)
print(g)

# s1='\141\142\143\x61\x62\x63'
# # 八进制97 98 99 十六进制 97 98 99
# print(s1)

# ASCII --> GB2321 --> GBK --> Unicode(UTF-8)多国语言
s2='\u9a86\u660a' # Unicode 编码
print(s2) # 骆昊 