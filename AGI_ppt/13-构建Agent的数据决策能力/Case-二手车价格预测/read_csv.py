"""
read_csv - 读取csv文件

Author: lsy
Date: 2026/2/10
"""
# pandas：Python 数据分析和处理库
import pandas as pd

# 读取CSV文件，指定分隔符
df = pd.read_csv('used_car_train_20200313.csv', sep=' ')

# 打印前5行数据
print("数据集前5行:")
print(df.head()) # 默认打印数据集的前 5 行

# 打印数据集基本信息
print("\\n数据集形状:", df.shape)
print("\\n数据列名:")
print(df.columns.tolist())
print("\\n数据类型:")
print(df.dtypes)

