"""
example01 - 分支结构（选择结构）的例子

Author: lsy
Date: 2025/12/3
"""
import getpass
# admin 123
username=input('用户名：')
password=input('密码：')
# password=getpass.getpass('密码：') # 掩码 终端运行

if username == 'admin' and password == '123':
    print('登录成功')
else:
    print('用户名或密码错误')
print('程序结束，再见！')