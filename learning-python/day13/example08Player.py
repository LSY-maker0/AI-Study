"""
example08Player - 玩家

Author: lsy
Date: 2025/12/10
"""
from example06Card import Card
from example07Poker import Poker

class Player:
    """玩家"""

    def __init__(self,nickname):
        self.nickname = nickname
        self.cards = []

    def get_one_card(self,card):
        """摸一张牌"""
        self.cards.append(card)

    def arrange(self):
        """玩家整理手上的牌"""
        self.cards.sort()

    def show(self):
        """显示玩家手里的牌"""
        print(self.nickname,end=':')
        for card in self.cards:
            print(card,end=' ')
        print()

def main():
    poker = Poker()
    poker.shuffle()
    nicknames=['张三','李四','王五','赵六']
    players=[Player(nickname) for nickname in nicknames]
    for _ in range(39//len(players)):
        for player in players:
            card=poker.deal()
            player.get_one_card(card)
    for player in players:
        player.arrange()
        player.show()

if __name__ == '__main__':
    main()

