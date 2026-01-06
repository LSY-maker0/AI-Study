"""
归档压缩 - shutil 模块（封装了高级的文件操作函数）

shutil.make_archive（归档加压缩）

Author: lsy
Date: 2026/1/6
"""
import shutil

# 获取命令的路径
# print(shutil.which('python'))
# 移动文件
# shutil.move('../resources/静夜思.txt','静夜思.txt')

def main():
    # 生成归档文件（带压缩）
    shutil.make_archive('../resources/images', 'zip', '../resources/images')

if __name__ == '__main__':
    main()