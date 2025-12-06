items = ['1', '2', '5', '4']
print(items)

# nums2=[int(x) for x in items]
# nums2.sort()
# nums3=[str(x) for x in nums2]
# print(nums3)


items.sort(key=int)  # 以什么方式排序
print(items)
