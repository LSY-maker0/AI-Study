"""
Poker - 扑克

Author: lsy
Date: 2025/12/10
"""
from Card01 import Card
import random

class Poker:

    def __init__(self):
        self.cards=[Card(suite,face) for suite in 'ABCD' for face in range(1,14)]
        self.counter = 0

    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards[self.counter]
        self.counter += 1
        return card

    def has_more(self)->bool:
        return self.counter<len(self.cards)

def main():
    poker=Poker()
    poker.shuffle()
    while poker.has_more():
        print(poker.deal(), end=' ')

if __name__ == '__main__':
    main()