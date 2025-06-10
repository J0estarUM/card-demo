from typing import List, Optional
from card import Card

class Pile:
    def __init__(self):
        self.cards: List[Card] = []  # 所有卡牌
        self.face_up_cards: List[Card] = []  # 正面朝上的卡牌
        
    def add_card(self, card: Card):
        """添加一张卡牌到牌堆"""
        self.cards.append(card)
        if card.face_up:
            self.face_up_cards.append(card)
            
    def remove_card(self, index: int) -> Optional[Card]:
        """从牌堆中移除指定位置的卡牌"""
        if 0 <= index < len(self.cards):
            card = self.cards.pop(index)
            if card in self.face_up_cards:
                self.face_up_cards.remove(card)
            return card
        return None
    def first_flip(self):
        if self.cards and not self.cards[-1].face_up:
            for i in range(-4,-1):
                self.cards[i].flip()
                self.face_up_cards.append(self.cards[i])
    def flip_top_card(self):
        """翻转顶部卡牌"""
        if self.cards and not self.cards[-1].face_up:
            self.cards[-1].flip()
            self.face_up_cards.append(self.cards[-1])
            
    def __len__(self):
        return len(self.cards)

    def add_card_to_bottom(self, card: Card):
        """将卡牌插入牌堆底部"""
        self.cards.insert(0, card)
        if card.face_up:
            self.face_up_cards.insert(0, card) 