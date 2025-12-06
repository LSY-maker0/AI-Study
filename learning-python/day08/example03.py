# 字符串方法 只能读不能改写
a = 'hello world'
# for i,str in enumerate(a):
#   print(i,str)

import time
import os # 操作系统
# 清屏命令 Windows --> cls / macos --> clear
import platform # 导入 platform 模块来识别操作系统


# def clear_screen():
#     """跨平台的清屏函数"""
#     # platform.system() 返回操作系统的名称，如 'Windows', 'Linux', 'Darwin' (macOS)
#     if platform.system() == 'Windows':
#         os.system('cls')
#     else:
#         os.system('clear')

# # 跑马灯效果
# content='拼搏到无能为力量，坚持到感动自己     '

# while True:
#   clear_screen()
#   content=content[1:]+content[0]
#   time.sleep(0.9) # 休眠，让程序暂停 500 ms
#   print(content)


# 跑马灯效果
content = '拼搏到无能为力，坚持到感动自己...     '

# 循环的次数可以设为无限，但这里用200次做演示
for i in range(200):
    # \r 让光标回到行首
    # end='' 防止 print 自动换行
    # flush=True 强制立即输出，防止缓冲
    # print('\r' + content, end='', flush=True)

    print('\r',content,end='',flush=True)
    
    # 在内存中更新字符串
    content = content[1:] + content[0]
    
    time.sleep(0.2)

# 循环结束后，打印一个换行符，以免命令行提示符跟在一行后面
print() 
  