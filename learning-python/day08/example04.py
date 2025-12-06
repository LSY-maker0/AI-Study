# a='abc'
# print(a.center(6,'*')) # .abc..
# print(a.rjust(6,'*')) # .abc..
# print(a.ljust(6,'*')) # .abc..

# b='123'
# print(b.zfill(6))

a=123
b=90

print('%d+%d=%d'%(a,b,a+b))
print('{}+{}={}'.format(a,b,a+b))
# print('{2}+{1}={0}'.format(a,b,a+b))

print(f'{a}+{b}={a+b}')
 