"""
Player - 玩家

Author: lsy
Date: 2025/12/10
"""

from Poker02 import Poker


class Player:
    def __init__(self,nickname):
        self.nickname = nickname
        self.card = []

    def get_one_card(self,card):
        self.card.append(card)

    def arrange(self):
        self.card.sort()

    def show(self):
        print(self.card)

def main():
    poker=Poker()
    poker.shuffle()
    nicknames=['张三','李四','王五']



