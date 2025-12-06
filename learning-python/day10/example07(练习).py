"""
# 赌博游戏

第一次摇出7或11玩家胜，1，3，5玩家输,其他点接着摇，摇到第一次的点玩家胜，摇到7玩家输
有1000块，下注
"""
import random

money=1000

while money>0:
  xiazhu=0
  print(f'当前余额:{money}')

  while xiazhu<=0 or xiazhu>money:
    try:
      xiazhu=int(input('请下注:'))
    except ValueError:
      pass

  first_point=random.randrange(1,7)+random.randrange(1,7)
  if first_point in (7,11):
    money+=xiazhu
    print('玩家胜')
  elif first_point in (1,3,5):
    money-=xiazhu
    print('玩家输')
  else:
    while True:
      curr_point=random.randrange(1,7)+random.randrange(1,7)
      if curr_point==first_point:
        money+=xiazhu
        print('玩家胜')
        break
      elif curr_point==7:
        money-=xiazhu
        print('玩家输')
        break
print('输光了啊啊')
  

  
list=[1,2,3,2]
print(random.choices(list,k=3))

print(list[-1])

a=2
b=int(input('输入'))
print(a is b)