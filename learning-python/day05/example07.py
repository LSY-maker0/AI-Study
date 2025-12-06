"""
example07 - 显示所有的汉字

汉字的编码范围：0x4e00 ～ 0x9fa5

ord()函数 --> 查看字符对应的编码
chr()函数 --> 将编码处理成对应的字符

Author: lsy
Date: 2025/12/4
"""

print(hex(ord('骆'))) # 16进制

# for i in range(0x4e00,0x9fa5):
#     print(chr(i),end='')
