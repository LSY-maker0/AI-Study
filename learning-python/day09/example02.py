set1={1,2,3,4,5}
set2={4,5,6,7}

# 交集
print(set1 & set2)
print(set1.intersection(set2))

# 并集
print(set1 | set2)
print(set1.union(set2))

# 差集
print(set1 - set2)
print(set1.difference(set2))

# 对称差
print(set1 ^ set2)
print((set1 | set2) - (set1 & set2))
print(set1.symmetric_difference(set2))

set3={1,2}
set4={1,2,3,4}

# 判断真子集 
print(set3<set4)

# 判断子集
print(set3<=set4)

# 判断超集
print(set3>set4)