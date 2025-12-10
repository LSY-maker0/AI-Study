"""
example06 - 

Author: lsy
Date: 2025/12/8
"""

# __init__ 初始化方法，创建对象时候自动调用
# __str__ 获得对象的字符串表示，调用print函数输出对象会被自动调用(放容器中就就不自动调用了)
# __repr__ 获得对象的字符串表示，把对象放到容器中，print输出时自动调用（都自动调用）
#     representation

from enum import Enum

class Suite(Enum):
    SPADE,HEART,CLUB,DIAMOND=range(4)

class Card:

    def __init__(self, suite, face):
        self.suite = suite
        self.face = face

    # def __str__(self):
    #     return self.show()

    def __repr__(self):
        return self.show()

    def __lt__(self, other):
        if self.suite == other.suite:
            return self.face < other.face
        return self.suite.value < other.suite.value

    def show(self):
        suits=['♠️','♥️','♣️','♦️']
        faces=['','A','2','3','4','5','6','7','8','9','10','J','Q','K']
        return f'{suits[self.suite.value]} {faces[self.face]}'


def main():
    card = Card( Suite.SPADE,9)
    print(card)

if __name__ == '__main__':
    main()