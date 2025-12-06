"""
str（字符串） --> encode(指定字符集，如UTF-8) --> bytes（字节串）
bytes（字节串） --> decode() --> str（字符串）

1. 选择字符集（编码）的时候，最佳选择（也是默认）UTF-8编码
2. 编码和解码的字符集要保持一致，否则乱码
3. 不能用ISO-8859-1编码保存中文，否则会出现编码黑洞，中文变成？。
4. UTF-8是一种变长的编码
数字字母最少1字节，中文3字节，Emoij4字节，有些两字节（'é' 的 UTF-8 编码: b'\xc3\xa9', 长度为: 2）
"""

'''
1. 百分号编码（URL Encoding）:用于url中安全地传输特殊字符（当url中包含空格，中文或特殊符号就需要百分号编码）
如：空格编码成 %20，'你'编码成%E4%BD%A0，&编码成%26
2. Base64编码：二进制转换为文本
只包含 A-Z,a-z,0-9,+,-,/,= 这些符号
编码后的数据比原始数据大 约33%
可逆，可以解码还原为原始数据
应用场景：将图片直接嵌入html，（Data URL），邮件系统中传输二进制文件，API接口传输中包含特殊字符的数据
'''

# 字符串的编码和解码（encode,decode）
# 编码解码方式统一，不然乱码

a='我是谁🤗❤️'
# print(a.encode('gbk')) # b'\xce\xd2\xca\xc7\xcb\xad'
# b=a.encode('gbk')
# print(b.decode('gbk')) # 我是谁
# print(b.decode('utf-8')) # 不一致会报错，UnicodeDecodeError

# UTF-8是一种变成编码
# 表示数字和英文字母的时候，一个字节
# 表示中文，三个字节
# 便是Emoij字符🤗❤️，四个字节
# 有些占两个字节

# ❤️ (红心) 这个 Emoji
# 基础的红心符号 ❤ (占用 3 个字节)
# 一个用于选择样式的修饰符 (占用 3 个字节)

# 一个emoij占四个字节
# utf-8 可以解码emoij字符
c=a.encode('utf-8') # b'\xe6\x88\x91\xe6\x98\xaf\xe8\xb0\x81'
print(len(c))
print(c.decode('utf-8')) # 我是谁


# 编码黑洞 （中文全变成？，想解码都没办法）
# b=a.encode('ios-8859-1') # LookupError: unknown encoding: ios-8859-1
# print(b)