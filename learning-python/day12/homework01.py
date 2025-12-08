"""
homework01 - 冒泡排序

设计函数的时候，一定要注意无副作用设计

Author: lsy
Date: 2025/12/7
"""
def bubble_sort(items:list,ascending=True,gt=lambda x,y:x>y) -> list:
    # 注意优化，无副作用性
    items = items[:] # 不改变原来的列表，赋给了一个新的变量
    for i in range (len(items)):
        swapped = False
        for j in range(len(items)-i-1):
            if gt(items[j],items[j+1]):
                items[j], items[j+1] = items[j+1], items[j]
                swapped = True
        if not swapped:
            break
    if not ascending:
        items=items[::-1]
    return items

if __name__ == '__main__':
    # print(bubble_sort([1, 2, 9, 3, 2, 4]))
    items=['apple','orange','water','fish']
    print(bubble_sort(items,True,lambda x,y:len(x)>len(y)))
