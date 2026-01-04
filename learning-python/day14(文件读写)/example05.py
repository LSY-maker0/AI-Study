"""
example05 - with 自动关闭文件（上下文语法）

Author: lsy
Date: 2026/1/5
"""
# 会自动执行file.close()
with open('resources/静夜思.txt','r') as f:
    for line in f:
        print(line)

