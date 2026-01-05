"""
example01 - Python操作Excel

三方库：
~ xlrd / xlwt / xlutils ---> 兼容低版本的Excel文件（xls）
~ openpyxl -> Office 2007+ -> xlsx

安装三方库：
pip install xlrd xlwt xlutils

Author: lsy
Date: 2026/1/5
"""
import xlrd

# 工作
wb = xlrd.open_workbook('../resources/员工信息表.xlsx')
print(wb.sheet_names())  # 获取所有工作表名字
sheet = wb.sheet_by_name('Sheet1')
# sheet = wb.sheet_by_index(0) # 拿第一个表
print(sheet.nrows, sheet.ncols) # 行数，列数


print(sheet.row(0)[1]) # 取第一行 第二列
print(sheet.row_slice(0,start_colx=0,end_colx=3)) # 第0列、第1列、第2列
print(sheet.col(4)) # 第五列

# 取单元格 --> cell
print(sheet.cell(1,2)) # 单元格对象
print(sheet.cell(2,2).value) # 值