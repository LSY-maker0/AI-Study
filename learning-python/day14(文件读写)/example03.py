"""
example03 - 读取文件，计算MD5哈希码，摘要

Author: lsy
Date: 2026/1/5
"""
from hashlib import md5,sha256

hasher=md5()
hasher2=sha256()
file = open('resources/apple.jpeg','rb')
try:
    data = file.read(512)
    while data:
        hasher.update(data)
        data = file.read(512)
finally:
    file.close()

# 获得十六进制形式的MD5哈希摘要
print(hasher.hexdigest()) # a21015ec27df24c93949b9650459365d
# sha256的摘要
print(hasher2.hexdigest()) # e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

