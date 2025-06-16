from typing import List, Tuple, Optional
import random
from card import Card
from pile import Pile
from player import Player
from config import MAX_HEALTH

class Game:
    def __init__(self):
        self.player = Player(max_hp=MAX_HEALTH)
        self.piles = [Pile() for _ in range(6)]  # 6个牌堆
        self.active_curse = None  # 当前激活的诅咒卡
        self.defense_cards = []  # 防御卡
        self.attack_cards = []   # 攻击卡
        self.settlement_area = []  # 结算区域
        self.removed_by_defense = []  # 被防御消灭的诅咒卡
        self.removed_by_attack = []   # 被攻击消灭的诅咒卡
        
        # 初始化游戏
        self.initialize_game()
        
    def initialize_game(self):
        """初始化游戏"""
        # 创建52张卡牌，数值范围1-16，类型随机
        card_types = ['attack', 'defense', 'curse', 'heal']
        total_cards = 52
        all_cards = []
        for _ in range(total_cards):
            card_type = random.choice(card_types)
            value = random.randint(1, 16)
            card = Card(card_type, value, face_up=False)
            all_cards.append(card)
        random.shuffle(all_cards)
        # 初始牌堆分布 [9,9,8,8,9,9]
        pile_counts = [9, 9, 8, 8, 9, 9]
        idx = 0
        for pile, count in zip(self.piles, pile_counts):
            for _ in range(count):
                pile.add_card(all_cards[idx])
                idx += 1
            pile.first_flip()

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
        """所有牌堆和结算区都没有诅咒卡即胜利"""
        for pile in self.piles:
            for card in pile.cards:
                if card.type == 'curse':
                    return False
        for card in self.settlement_area:
            if card.type == 'curse':
                return False
        return True

    def add_to_settlement(self, cards: List[Card]) -> Tuple[bool, str]:
        """将一组卡牌添加到结算区域并立即处理效果（新规则）"""
        if not cards:
            return False, "No cards to process"

        # 统计本次拖入的诅咒卡、攻击卡、防御卡
        curse_cards = [c for c in cards if c.type == 'curse']
        attack_cards = [c for c in cards if c.type == 'attack']
        defense_cards = [c for c in cards if c.type == 'defense']
        other_cards = [c for c in cards if c.type not in ('curse', 'attack', 'defense')]
        msg_list = []

        # 1. 处理诅咒卡：加入结算区
        if curse_cards:
            self.settlement_area.extend(curse_cards)
            msg_list.append(f"拖入{len(curse_cards)}张诅咒卡，等待结算。")

        # 2. 处理防御+攻击卡（与结算区已有诅咒卡互动）
        exist_curse = [c for c in self.settlement_area if c.type == 'curse']
        if defense_cards or attack_cards:
            remain_curse_cards = sorted(exist_curse, key=lambda x: x.value)
            removed_by_defense = []
            removed_by_attack = []
            returned_curse = []
            remain_defense = sum(c.value for c in defense_cards)
            remain_attack = sum(c.value for c in attack_cards)
            # 先用防御抵消诅咒卡
            for curse in remain_curse_cards:
                if remain_defense >= curse.value:
                    remain_defense -= curse.value
                    removed_by_defense.append(curse)
                else:
                    break
            # 更新剩余未被防御抵消的诅咒卡
            remain_curse_cards = [c for c in remain_curse_cards if c not in removed_by_defense]
            # 再用攻击消灭诅咒卡
            for curse in remain_curse_cards:
                if remain_attack >= curse.value:
                    remain_attack -= curse.value
                    removed_by_attack.append(curse)
                else:
                    returned_curse.append(curse)
            # 更新结算区，移除被消灭和返回的诅咒卡
            self.settlement_area = [c for c in self.settlement_area if c.type != 'curse']
            # 更新被消灭的诅咒卡列表
            self.removed_by_defense.extend(removed_by_defense)
            self.removed_by_attack.extend(removed_by_attack)
            # --- 修改：返回的诅咒卡放入随机牌堆底部 ---
            for curse in returned_curse:
                random_pile = random.choice(self.piles)
                random_pile.add_card_to_bottom(curse)
            # 玩家只扣未被抵消/消灭的诅咒牌的总和
            total_damage = sum(c.value for c in returned_curse)
            if removed_by_defense:
                msg_list.append(f"防御成功抵消{len(removed_by_defense)}张诅咒卡。")
            if removed_by_attack:
                msg_list.append(f"攻击消灭{len(removed_by_attack)}张诅咒卡。")
            if returned_curse:
                if total_damage > 0:
                    self.player.take_damage(total_damage)
                    msg_list.append(f"仍有{len(returned_curse)}张诅咒卡未被消灭，已返回随机牌堆，受到{total_damage}点伤害。")
                else:
                    msg_list.append(f"仍有{len(returned_curse)}张诅咒卡未被消灭，已返回随机牌堆。")
            if not (removed_by_defense or removed_by_attack or returned_curse):
                msg_list.append("结算区没有诅咒卡，无需结算。")
        # --- 新增：只拖入诅咒牌时也立即结算 ---
        elif curse_cards:
            # 只拖入诅咒牌，全部返回随机牌堆底部并扣血
            total_damage = sum(c.value for c in curse_cards)
            for curse in curse_cards:
                random_pile = random.choice(self.piles)
                random_pile.add_card_to_bottom(curse)
            self.settlement_area = [c for c in self.settlement_area if c.type != 'curse']
            if total_damage > 0:
                self.player.take_damage(total_damage)
                msg_list.append(f"诅咒卡直接结算，已返回随机牌堆，受到{total_damage}点伤害。")
        # 其他卡牌（如治疗）
        for card in other_cards:
            if card.type == 'heal':
                self.player.heal(card.value)
                msg_list.append(f"治疗{card.value}点生命值。")
        if msg_list:
            return True, ' '.join(msg_list)
        else:
            return False, "未产生结算效果。"

    def get_total_curse_value(self, include_removed: bool = False) -> int:
        """统计诅咒牌的数值总和
        
        Args:
            include_removed: 是否包括被消灭的诅咒卡（默认False）
        """
        total = 0
        if include_removed:
            # 统计被消灭的诅咒卡
            total += sum(c.value for c in self.removed_by_attack)
        else:
            # 统计牌堆中的诅咒卡
            for pile in self.piles:
                total += sum(card.value for card in pile.cards if card.type == 'curse')
        return total

