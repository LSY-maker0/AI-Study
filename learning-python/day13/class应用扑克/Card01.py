"""
Card - 卡片类

Author: lsy
Date: 2025/12/10
"""

class Card:
    def __init__(self,suite,face):
        self.suite=suite
        self.face=face


    def __repr__(self):
        return self.show()

    def show(self):
        suits={'A':'♠️','B':'♥️','C':'♣️','D':'♦️'}
        faces=['','A','2','3','4','5','6','7','8','9','10','J','Q','K']
        return f'{suits[self.suite]} {faces[self.face]}'

def main():
    card=Card('B',2)
    print(card)

if __name__ == '__main__':
    main()
