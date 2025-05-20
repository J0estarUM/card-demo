from config import CARD_TYPES, CARD_VALUES

class Card:
    def __init__(self, card_type: str, value: int, face_up: bool = True):
        if card_type not in CARD_TYPES:
            raise ValueError(f"无效的卡牌类型: {card_type}")
        if value not in CARD_VALUES:
            raise ValueError(f"无效的卡牌数值: {value}")
        
        self.type = card_type
        self.value = value
        self.face_up = face_up
    
    def flip(self):
        """翻转卡牌"""
        self.face_up = not self.face_up
    
    def __str__(self):
        return f"{self.type}({self.value})"
    
    def __repr__(self):
        return self.__str__() 