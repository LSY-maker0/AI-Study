"""
example02 - 获取指定文件夹下的所有文件

Author: lsy
Date: 2026/1/6
"""
from pathlib import Path
import os

print(os.path.abspath(__file__)) # 拿到绝对路径
print(os.listdir('../')) # ['example02.py', 'example01.py']
files_list = os.listdir()
for file in files_list:
    print(file,os.path.isdir(file)) # 是否是文件夹
    print(file,os.path.isfile(file)) # 是否是文件


# path = Path('../resources')
#
# for item in path.iterdir():
#     print(item)
