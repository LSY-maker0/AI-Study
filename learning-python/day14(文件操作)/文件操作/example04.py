"""
example04 - 写文本文件

Author: lsy
Date: 2026/1/5
"""
file = open('../resources/小雨康桥的诗.txt', 'w')

try:
    file.write('我想做燕子\r\n')
    file.write('只需简单思想\r\n')
finally:
    file.close()


file1 = open('../resources/小雨康桥的诗.txt', 'a') # append 指针移到文件末尾，接着写
try:
    file1.write('我不想做燕子\r\n')
    file1.write('不只需简单思想\r\n')
finally:
    file1.close()