"""
example07 - 扑克

Author: lsy
Date: 2025/12/9
"""
import random
from example06Card import Card
from example06Card import Suite

class Poker:
    """扑克"""

    def __init__(self):
        self.cards = [Card(suit, face)
                      for suit in Suite
                      for face in range(1, 14)]
        # for suit in 'SHCD':
        #     for face in range(1,14):
        #         card=Card(suit,face)
        #         self.cards.append(card)
        self.counter = 0

    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)

    def deal(self):
        """发牌"""
        card = self.cards[self.counter]
        self.counter += 1
        return card

    def has_more(self) -> bool:
        """是否还有牌"""
        return self.counter < len(self.cards)


def main():
    poker = Poker() # 创建扑克
    poker.shuffle() # 洗牌
    while poker.has_more(): # 发牌
        print(poker.deal(),end=' ')


if __name__ == '__main__':
    main()
