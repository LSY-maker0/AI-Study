"""
Python数据类型

Author：lsy
Date：2025.12.3
"""


a=123
b=1.23
c='hello'
d=True
e=3+5j

# # int ---> integer 整型
# print(a,type(a))
# # float 浮点型
# print(b,type(b))
# # str ---> string 字符串型
# print(c,type(c))
# # bool ---> boolean 布尔型（True/False）
# print(d,type(d))
# # complex（复数类型） 复数类型
# print(e,type(e))
#
#
# e='goodbye'
# print(e,type(e))


"""
1. 数字类型 (Numeric Types)
int (整数): 比如 10, -5, 0
float (浮点数): 比如 3.14, -0.001
complex (复数): 比如 2 + 3j (在科学计算和数据分析中会用到)
bool (布尔值): True 和 False，它的本质是整数 (True就是1, False就是0)。
"""

"""
2. 序列类型 (Sequence Types)
这类类型的特点是元素有序，可以用索引（比如 my_list[0]）来访问。
str (字符串): 比如 "hello", '前端开发'
list (列表): 比如 [1, "vue", True]，可变的，里面的元素可以增删改。
tuple (元组): 比如 (1, "vue", True)，不可变的，一旦创建就不能修改。
"""

"""
3. 集合类型 (Set Types)
这类类型的特点是元素无序且不重复。

set (集合): 比如 {1, 2, 3}，可变。
frozenset (冻结集合): 比如 frozenset({1, 2, 3})，不可变。
"""

"""
4. 映射类型 (Mapping Types)
dict (字典): 存储键值对 (key-value)，比如 {"name": "张三", "age": 25}。键必须是不可变类型，值可以是任意类型。可变。
"""

"""
5. 其他核心内置类型
NoneType: 只有一个值 None，表示“空”或“无”。
object: 所有Python对象的“老祖宗”，是所有类的基类。
"""
