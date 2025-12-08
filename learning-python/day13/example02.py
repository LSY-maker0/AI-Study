"""
example02 - 创建对象 / 给对象发消息

Author: lsy
Date: 2025/12/8
"""
from example01 import Student

# 创建对象 --> 构造器语法 --> 类名（..）
stu1=Student('张三',12)
# 发出消息
stu1.study('英语')


# Student.study(stu1,'语文')
