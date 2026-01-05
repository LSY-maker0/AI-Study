"""
example02 - 读word文档

Author: lsy
Date: 2026/1/6
"""
from docx import Document

# 打开已有文档
doc = Document('../resources/demo.docx')

# 遍历所有段落，获取文本
for para in doc.paragraphs:
    print(para.text)