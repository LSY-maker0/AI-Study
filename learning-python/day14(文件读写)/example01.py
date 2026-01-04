"""
example01 - 文件操作

'r' ： 读取（默认）
'w' ： 写入（会覆盖之前的内容）
'x' ： 写入（如果已存在显示异常）
'a' ： 追加（内容写在文件末尾）
'b' ： 二进制模式
't' ： 文本模式（默认）
'+' ： 更新（既可以读也可以写）

Author: lsy
Date: 2026/1/4
"""
import sys

print(sys.getdefaultencoding())
file = open('resources/静夜思.txt', 'r', encoding='utf-8')
try:
    # print(file.read(12),end="")  # 读文件 指定每次读12个字符
    data = file.read(12) # 如果读不到数据，read方法会返回None
    while data:
        print(data,end="")
        data = file.read(12)

except:
    print('读文件时发生错误')
finally:
    file.close() # 关闭文件


# with open('./静夜思.txt', 'w', encoding='utf-8') as f:
#     f.write("""静夜思
# 床前明月光，
# 疑是地上霜。
# 举头望明月，
# 低头思故乡。""")

