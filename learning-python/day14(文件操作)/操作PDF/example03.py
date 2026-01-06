"""
example03 - 创建pdf文档 reportlab

Author: lsy
Date: 2026/1/7
"""
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont

# 1. 指定保存路径
pdf_file = '../resources/我是新建的PDF.pdf'

# 2. 创建画布 (A4 纸大小: 595 x 842 点)
c = canvas.Canvas(pdf_file, pagesize=(595, 842))

# 3. 绘制内容
# 设置字体 (Helvetica, 大小 20)
c.setFont("Helvetica", 20)
# 画文字 (x坐标, y坐标, 内容)
# 注意：PDF 坐标原点 (0,0) 在**左下角**
c.drawString(100, 750, "Hello, 这是我用 Python 创建的 PDF！")
c.drawString(100, 720, "2024-05-24")

# 4. 保存并关闭
c.save()

print(f'PDF 已生成: {pdf_file}')
