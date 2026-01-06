"""
example06.py - 销售记录表 操作，统计

Author: lsy
Date: 2026/1/6
"""
import openpyxl

wb=openpyxl.load_workbook('../resources/销售记录.xlsx')
sheet=wb.worksheets[0]

sheet['G1']='总量'
for i in range(2,6):
    sheet[f'G{i}']=f'=average(C{i}:D{i})'

wb.save('../resources/销售记录.xlsx')