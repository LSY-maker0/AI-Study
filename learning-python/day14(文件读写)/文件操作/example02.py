"""
example02 - 读二进制文件

文件的 MD5 码（指纹，签名），下载时先对这个码 SHA-256

Author: lsy
Date: 2026/1/5
"""
from os import SEEK_END, SEEK_SET

file = open(file='../resources/apple.jpeg', mode='rb')
file.seek(0,SEEK_END) # 从0移动到文件末尾
print(file.tell())  # 移动的字节数 6185字节
file.seek(0,SEEK_SET)
try:
    data=file.read(512)
    while data:
        print(data,end="\n")
        data=file.read(512)
finally:
    file.close()

