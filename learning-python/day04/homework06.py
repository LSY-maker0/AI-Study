"""
homework06 - 百钱百鸡问题

鸡翁一值钱5，鸡母一值钱3，鸡雏三值钱1，用百钱买百鸡，问鸡翁，鸡母，鸡雏各几只

Author: lsy
Date: 2025/12/3
"""
import time
# start = time.time()
# for i in range(0, 20):
#     for j in range(0, 33):
#         for k in range(0, 300,3):
#             if i+j+k == 100 and 5*i+3*j+k//3 == 100:
#                 print(i,j,k)
# end = time.time()
# print(end-start) # 0.0068149566650390625

start = time.time()
for i in range(0, 20):
    for j in range(0, 33):
        k=100-i-j
        if k%3==0 and 5*i+3*j+k//3==100:
            print(i,j,k)
end = time.time()
print(end - start) # 0.0002009868621826172