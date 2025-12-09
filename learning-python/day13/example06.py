"""
example06 - 

Author: lsy
Date: 2025/12/8
"""

class Poker:
    """扑克"""

    def __init__(self):
        self.card = []
        for suit in 'SHCD':
            for face in range(1,14):
                card=Card(suit,face)
                self.card.append(card)