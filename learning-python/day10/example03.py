import string
str='fhuiahfuiahfuihauifhuiadaaaaaaaaaaaaaaaaaaaaaaaa'

result={letter:0 for letter in string.ascii_letters}
for ch in str:
  if ch in result:
    result[ch]+=1

for key,value in result.items():
  print(f'{key}出现了：{value:>2d}次') # 右对齐占2个位置
# print(result)