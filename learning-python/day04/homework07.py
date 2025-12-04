"""
homework07 -

五个人（ABCDE）晚上去捕鱼，铺了不计其数的鱼，然后累了去睡觉
第二天，A第一个醒来，把鱼分成了5份，扔掉了多余的1条，然后拿走自己的1份
B第二个醒来，以为鱼没有分过，把剩下的鱼分成了5份，扔掉了多余的1条，拿走了自己的1份
C，D，E依次醒过来，都按照同样的方法来分鱼。问他们最小捕了多少条鱼？

Author: lsy
Date: 2025/12/3
"""

fish = 6
while True:
    is_enough = True

    # 判断是否够分
    total = fish
    for _ in range(5):  # 0到4 不关心下标，只关心循环了几次
        if (total - 1) % 5 == 0:
            total = 4 * (total - 1) // 5
        else:
            is_enough = False
            break

    if is_enough:
        print(fish)
        break
    fish += 5
