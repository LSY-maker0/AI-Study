"""
example08 - 读取CSV（逗号分隔值）文件

Author: lsy
Date: 2026/1/5
"""
import csv

# with open("resources/temperature.txt",'w') as f:
#     reader = csv.reader(f,delimiter='#',quotechar='"') # 通过#来分隔,把 " 去掉
#     for row in reader:
#         print(row)

with open("../resources/temperature.txt") as f1:
    with open("../resources/temperature2.csv", "w") as f2:
        writer = csv.writer(f2,delimiter=',') # 写csv文件
        writer.writerow(['ID','temperature','text','string','label'])
        content = f1.readline()
        while content:
            no,temperature,text,string,label = content.split(' ')
            writer.writerow([no,temperature,text,string,label])
            content = f1.readline()