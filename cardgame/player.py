from typing import List, Tuple
from card import Card
from music_handler import music_handler

class Relic:
    def __init__(self, name: str, description: str, trigger_type: str):
        self.name = name
        self.description = description
        self.trigger_type = trigger_type  # 'click' 或 'auto'
        self.charges = 0  # 遗物使用次数
        self.max_charges = 3  # 最大使用次数

    def trigger(self) -> Tuple[bool, str]:
        """触发遗物效果"""
        if self.charges >= self.max_charges:
            return False, f"{self.name} has reached maximum uses"
        self.charges += 1
        return True, f"{self.name} effect activated!"

class Player:
    def __init__(self, max_hp: int = 100,hp:int = 5):
        self.max_hp = max_hp
        self.hp = hp
        self.relics: List[Relic] = []
        self.initialize_relics()

    def initialize_relics(self):
        """初始化遗物"""
        # 点击触发型遗物
        self.relics.append(Relic(
            "Healing Stone",
            "Click to restore 5 HP",
            "click"
        ))
        self.relics.append(Relic(
            "Power Stone",
            "Click to double the damage of next attack card",
            "click"
        ))
        
        # 自动触发型遗物
        self.relics.append(Relic(
            "Guardian Stone",
            "Gain 2 shield after each settlement",
            "auto"
        ))
        self.relics.append(Relic(
            "Lucky Stone",
            "20% chance to gain bonus effect after settlement",
            "auto"
        ))

    def take_damage(self, damage: int) -> int:
        """受到伤害"""
        self.hp = max(0, self.hp - damage)
        music_handler.play_sound("assets/music/health.mp3")
        return damage

    def heal(self, amount: int) -> int:
        """恢复生命值"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        music_handler.play_sound("assets/music/health.mp3")
        return self.hp - old_hp

    def get_relic(self, index: int) -> Relic:
        """获取指定索引的遗物"""
        if 0 <= index < len(self.relics):
            return self.relics[index]
        return None

    def add_relic(self, relic: Relic):
        """添加遗物"""
        if relic not in self.relics:
            self.relics.append(relic)
            
    def remove_relic(self, relic: Relic):
        """移除遗物"""
        if relic in self.relics:
            self.relics.remove(relic)
            
    def is_alive(self) -> bool:
        """检查玩家是否存活"""
        return self.hp > 0 