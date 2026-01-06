"""
example03 - python中的日期

Author: lsy
Date: 2026/1/5
"""
from datetime import datetime

date1=datetime(1990,5,3)
date2=datetime(2000,1,1,12,24,45)
date3=datetime.now()
print(date1)
print(date2)
print(date3)

delta = date3 - date1
print(delta,type(delta))
print(delta.days,delta.seconds)

# 格式化时间日期
from datetime import datetime

# 获取当前时间
date2 = datetime.now()

# 格式化输出
print(date2.strftime("%Y年%m月%d日 %H时%M分%S秒"))

