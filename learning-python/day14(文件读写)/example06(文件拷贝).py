"""
example06(文件拷贝) - 文件拷贝

Author: lsy
Date: 2026/1/5
"""

def file_copy(source_file,target_file):
    with open(source_file, 'rb') as source:
        with open(target_file, 'wb') as target:
            data = source.read(512)
            # for _ in range(5): # 显示一部分图片
            #     target.write(data)
            #     data = source.read(512)
            while data:
                target.write(data)
                data = source.read(512)

if __name__ == '__main__':
    file_copy('resources/apple.jpeg','source/apple.jpeg')
