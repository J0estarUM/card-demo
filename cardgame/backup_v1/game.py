from typing import List, Tuple, Optional
import random
from card import Card
from pile import Pile
from player import Player

class Game:
    def __init__(self):
        self.player = Player()
        self.piles = [Pile() for _ in range(6)]  # 6个牌堆
        self.active_curse = None  # 当前激活的诅咒卡
        self.defense_cards = []  # 防御卡
        self.attack_cards = []   # 攻击卡
        self.settlement_area = []  # 结算区域
        
        # 初始化游戏
        self.initialize_game()
        
    def initialize_game(self):
        """初始化游戏"""
        # 创建卡牌
        card_types = ['attack', 'defense', 'curse', 'heal']
        for pile in self.piles:
            # 每个牌堆添加10张随机卡牌
            for _ in range(10):
                card_type = random.choice(card_types)
                value = random.randint(1, 10)
                card = Card(card_type, value, face_up=False)
                pile.add_card(card)
            # 翻开顶部卡牌
            pile.flip_top_card()
            
    def move_cards(self, from_pile: int, to_pile: int, start_card_index: int) -> Tuple[bool, str]:
        """移动一组卡牌"""
        if not (0 <= from_pile < len(self.piles) and 0 <= to_pile < len(self.piles)):
            return False, "Invalid pile index"
            
        source_pile = self.piles[from_pile]
        target_pile = self.piles[to_pile]
        
        # 检查起始索引是否有效
        if start_card_index >= len(source_pile.face_up_cards):
            return False, "Invalid card index"
            
        # 计算要移动的卡牌数量（最多5张）
        top_index = len(source_pile.face_up_cards) - 1
        cards_to_move = source_pile.face_up_cards[start_card_index:min(start_card_index + 5, top_index + 1)]
        
        # 检查移动是否合法
        if not self.is_valid_move(cards_to_move, target_pile):
            return False, "Invalid move"
            
        # 执行移动
        for card in cards_to_move:
            source_pile.remove_card(source_pile.cards.index(card))
            target_pile.add_card(card)
        
        # 如果源牌堆还有卡牌，翻开顶部卡牌
        if source_pile.cards and not source_pile.face_up_cards:
            source_pile.flip_top_card()
            
        return True, "Move successful"
        
    def is_valid_move(self, cards: List[Card], target_pile: Pile) -> bool:
        """检查移动是否合法"""
        # 如果目标牌堆为空，可以移动
        if not target_pile.face_up_cards:
            return True
            
        # 获取源卡牌和目标牌堆顶部卡牌的值
        source_value = cards[0].value
        target_value = target_pile.face_up_cards[-1].value
        
        # 只能移动到数值更大的牌堆
        return source_value < target_value
        
    def check_game_over(self) -> bool:
        """检查游戏是否结束"""
        return not self.player.is_alive()
        
    def check_win_condition(self) -> bool:
        """检查是否满足胜利条件"""
        # 这里可以添加胜利条件
        return False 

    def add_to_settlement(self, cards: List[Card]) -> Tuple[bool, str]:
        """将一组卡牌添加到结算区域并立即处理效果"""
        if not cards:
            return False, "No cards to process"
            
        total_attack = 0
        total_defense = 0
        total_heal = 0
        has_curse = False
        
        # 计算各种类型的总值
        for card in cards:
            if card.type == 'attack':
                total_attack += card.value
            elif card.type == 'defense':
                total_defense += card.value
            elif card.type == 'heal':
                total_heal += card.value
            elif card.type == 'curse':
                has_curse = True
                total_attack += card.value * 2  # 诅咒卡造成双倍伤害
        
        # 应用效果
        if has_curse:
            self.player.take_damage(total_attack)
            return True, f"Curse activated! Dealt {total_attack} damage"
        else:
            if total_attack > 0:
                self.player.take_damage(total_attack)
            if total_defense > 0:
                self.player.heal(total_defense)
            if total_heal > 0:
                self.player.heal(total_heal)
                
            # 构建效果消息
            effects = []
            if total_attack > 0:
                effects.append(f"Dealt {total_attack} damage")
            if total_defense > 0:
                effects.append(f"Defended {total_defense}")
            if total_heal > 0:
                effects.append(f"Healed {total_heal}")
                
            return True, " and ".join(effects) if effects else "No effect"

