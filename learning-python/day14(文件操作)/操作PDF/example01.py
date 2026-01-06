"""
example01 - 读取PDF并抽取文字

pip install PyPDF2

Author: lsy
Date: 2026/1/6
"""
import PyPDF2

# 读取PDF方法
# reader = PyPDF2.PdfReader('../resources/浦发上海浦东发展银行西安分行个金客户经理考核办法.pdf')
# print(len(reader.pages))
#
# for i in range(len(reader.pages)):
#     page = reader.pages[i]  # 直接用索引获取
#     text = page.extract_text()
#     print(f'第 {i + 1} 页: {text}')

# 文件密码加密
reader = PyPDF2.PdfReader('../resources/浦发上海浦东发展银行西安分行个金客户经理考核办法.pdf')
writer = PyPDF2.PdfWriter()

for i in range(len(reader.pages)):
    writer.add_page(reader.pages[i])

# pdf加密
# writer.encrypt('123')
with open('../resources/浦发加密.pdf', 'wb') as f:
    writer.write(f)