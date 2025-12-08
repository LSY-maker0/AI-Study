"""
homework02(优化版代码面试) - 冒泡优化版的代码

Author: lsy
Date: 2025/12/7
"""

def bubble_sort(items,ascending=True,gt=lambda x,y:x>y):
    """
    冒泡排序
    :param items: 待排序列表
    :param ascending: 是否使用升序
    :param gt: 比较两个元素大小的函数
    :return: 排序后的列表
    """
    items=items[:]
    for i in range(len(items)):
        swapped=False
        for j in range(len(items)-i-1):
            if gt(items[j],items[j+1]):
                items[j],items[j+1]=items[j+1],items[j]
                swapped=True
        if not swapped:
            break
    if not ascending:
        items=items[::-1]
    return items

if __name__ == '__main__':
    items=['apple','orange','water','fish']
    print(bubble_sort(items,True,gt=lambda x,y:len(x)>len(y)))
