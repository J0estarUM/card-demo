from typing import List

class Player:
    def __init__(self, max_hp: int = 100, energy: int = 3):
        self.max_hp = max_hp
        self.hp = max_hp
        self.energy = energy
        self.max_energy = energy
        self.relics: List[str] = []  # 遗物列表
        self.hand = []  # 新增：手牌列表
        
    def take_damage(self, damage: int):
        """受到伤害"""
        self.hp = max(0, self.hp - damage)
        
    def heal(self, amount: int):
        """恢复生命值"""
        self.hp = min(self.max_hp, self.hp + amount)
        
    def add_relic(self, relic: str):
        """添加遗物"""
        if relic not in self.relics:
            self.relics.append(relic)
            
    def remove_relic(self, relic: str):
        """移除遗物"""
        if relic in self.relics:
            self.relics.remove(relic)
            
    def is_alive(self) -> bool:
        """检查玩家是否存活"""
        return self.hp > 0 