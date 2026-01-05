"""
example07 - 

Author: lsy
Date: 2026/1/5
"""
with open('../resources/temperature.txt', 'w') as f:
    for index in range(1,40):
        f.write(f'病人00{index} {index} 摄氏度\n')


processed_lines = []

# 将病人度数为偶数的温度打印出来
with open('../resources/temperature.txt', 'r') as f:
    line = f.readline()
    while line:
        clean_line = line.strip()
        temp=int(clean_line.split(' ')[1])
        if temp<=20:
            mark='低温'
        elif temp<=30:
            mark='中温'
        else:
            mark='高温'
        new_line = clean_line + ' - ' + mark + '\n'
        processed_lines.append(new_line)
        line = f.readline()

with open('../resources/temperature.txt', 'w') as f:
    f.writelines(processed_lines)

print('处理完成')
