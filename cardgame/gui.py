import pygame
import sys
import os
from typing import Tuple, Optional, Dict
from game import Game
from card import Card


# 资源管理类
class AssetManager:
    def __init__(self):
        self.images: Dict[str, pygame.Surface] = {}
        self.card_images: Dict[str, Dict[str, pygame.Surface]] = {}
        self.ui_elements: Dict[str, pygame.Surface] = {}
        self.backgrounds: Dict[str, pygame.Surface] = {}

        # 设置资源目录
        self.asset_dir = os.path.join(os.path.dirname(__file__), 'assets')
        self.create_asset_directories()

    def create_asset_directories(self):
        """创建资源目录结构"""
        directories = [
            os.path.join(self.asset_dir, d)
            for d in ['cards', 'backgrounds', 'ui', 'effects']
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def load_card_image(self, card_type: str, card_name: str) -> Optional[pygame.Surface]:
        """加载卡牌图片"""
        path = os.path.join(self.asset_dir, 'cards', f"{card_type}_{card_name}.png")
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            if card_type not in self.card_images:
                self.card_images[card_type] = {}
            self.card_images[card_type][card_name] = image
            return image
        return None

    def load_background(self, name: str) -> Optional[pygame.Surface]:
        """加载背景图片"""
        path = os.path.join(self.asset_dir, 'backgrounds', f"{name}.png")
        if os.path.exists(path):
            image = pygame.image.load(path).convert()
            self.backgrounds[name] = image
            return image
        return None

    def load_ui_element(self, name: str) -> Optional[pygame.Surface]:
        """加载UI元素"""
        path = os.path.join(self.asset_dir, 'ui', f"{name}.png")
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            self.ui_elements[name] = image
            return image
        return None


# 颜色定义
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'GRAY': (200, 200, 200),
    'LIGHT_BLUE': (173, 216, 230),
    'YELLOW': (255, 255, 0)
}

# 卡牌类型颜色映射
CARD_COLORS = {
    'attack': (255, 100, 100),  # 红色系
    'defense': (100, 100, 255),  # 蓝色系
    'curse': (100, 100, 100),  # 灰色系
    'heal': (100, 255, 100)  # 绿色系
}


class CardGUI:
    def __init__(self, card, x, y, width=100, height=150):
        self.card = card
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.original_x = x
        self.original_y = y
        self.is_top_card = False  # 新增：是否是牌顶的牌
        self.cards_above = []  # 新增：存储上面的牌

    def draw(self, screen):
        # 绘制卡牌背景
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        
        # 绘制卡牌名称
        font = pygame.font.Font(None, 24)
        name_text = font.render(self.card.name, True, (0, 0, 0))
        screen.blit(name_text, (self.x + 10, self.y + 10))
        
        # 绘制卡牌描述
        desc_font = pygame.font.Font(None, 18)
        desc_text = desc_font.render(self.card.description, True, (0, 0, 0))
        screen.blit(desc_text, (self.x + 10, self.y + 40))
        
        # 绘制卡牌类型
        type_text = font.render(self.card.card_type, True, (0, 0, 0))
        screen.blit(type_text, (self.x + 10, self.y + 120))

    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)

    def start_drag(self, pos):
        if not self.is_top_card:  # 只有牌顶的牌可以拖动
            return False
        self.dragging = True
        self.drag_offset_x = self.x - pos[0]
        self.drag_offset_y = self.y - pos[1]
        return True

    def drag(self, pos):
        if self.dragging:
            self.x = pos[0] + self.drag_offset_x
            self.y = pos[1] + self.drag_offset_y
            # 移动上面的牌
            for card in self.cards_above:
                card.x = self.x
                card.y = self.y - 20  # 每张牌向上偏移20像素

    def stop_drag(self):
        self.dragging = False
        self.x = self.original_x
        self.y = self.original_y
        # 重置上面的牌的位置
        for i, card in enumerate(self.cards_above):
            card.x = self.original_x
            card.y = self.original_y - 20 * (i + 1)


class GameGUI:
    def __init__(self, game: Game):
        pygame.init()
        self.game = game
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Card Game")
        self.clock = pygame.time.Clock()

        # 初始化资源管理器
        self.assets = AssetManager()

        # 卡牌尺寸
        self.card_width = 100
        self.card_height = 150
        self.card_scale = 1.0
        self.hover_scale = 1.2

        # 字体
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        self.tiny_font = pygame.font.Font(None, 18)  # 新增：更小的字体

        # 拖拽相关
        self.dragging = False
        self.drag_card = None
        self.drag_start_pos = None
        self.drag_offset = (0, 0)
        self.hovered_card = None

        # 底部区域布局
        self.bottom_area_height = 200
        self.bottom_area_rect = pygame.Rect(
            0,
            self.screen_height - self.bottom_area_height,
            self.screen_width,
            self.bottom_area_height
        )

        # 结算区域（左侧）
        self.settlement_area_rect = pygame.Rect(
            340,  # 左侧，增加边距
            self.screen_height - self.bottom_area_height + 10,  # 增加上边距
            500,  # 增加宽度
            self.bottom_area_height - 20  # 高度
        )

        # 生命值区域（中间）
        self.hp_area_rect = pygame.Rect(
            30,  # 中间，调整位置
            self.screen_height - self.bottom_area_height + 10,  # 增加上边距
            220,  # 增加宽度
            self.bottom_area_height - 20  # 高度
        )

        # 遗物区域（右侧）
        self.relic_area_rect = pygame.Rect(
            self.screen_width - 320,  # 右侧，调整位置
            self.screen_height - self.bottom_area_height + 10,  # 增加上边距
            290,  # 增加宽度
            self.bottom_area_height - 20  # 高度
        )

        # 牌堆区域（上移）
        self.pile_area_y = 50  # 原来是200

        # 视觉效果
        self.effects = []
        self.effect_duration = 1000  # 效果持续时间（毫秒）
        
        # 初始化界面
        self.initialize_gui()

    def initialize_gui(self):
        """初始化GUI资源"""
        # 加载背景
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(COLORS['WHITE'])

        # 加载卡牌背面
        self.card_back = pygame.Surface((self.card_width, self.card_height))
        self.card_back.fill(COLORS['BLUE'])
        pygame.draw.rect(self.card_back, COLORS['BLACK'], self.card_back.get_rect(), 2)

        # 加载生命值条
        self.hp_bar = pygame.Surface((0,0))
        self.hp_bar.fill(COLORS['GRAY'])

        # 加载遗物框
        self.relic_frame = pygame.Surface((50, 50))
        self.relic_frame.fill(COLORS['YELLOW'])
        pygame.draw.rect(self.relic_frame, COLORS['BLACK'], self.relic_frame.get_rect(), 2)

    def get_card_rect(self, pile_index: int, card_index: int) -> pygame.Rect:
        """获取卡牌在屏幕上的矩形区域"""
        x = 50 + pile_index * (self.card_width + 20)
        base_y = self.pile_area_y
        
        # 计算暗牌数量
        pile = self.game.piles[pile_index]
        hidden_cards_count = len(pile.cards) - len(pile.face_up_cards)
        
        # 计算卡牌位置
        y = base_y + (hidden_cards_count + card_index) * 30
        if card_index == len(pile.face_up_cards) - 1:  # 如果是顶部的牌
            y += 20  # 位置靠下一些
            
        return pygame.Rect(x, y, self.card_width, self.card_height)

    def get_card_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """获取指定位置的卡牌（只允许点击未被遮挡的部分）"""
        x, y = pos
        for pile_index, pile in enumerate(self.game.piles):
            for card_index, _ in enumerate(pile.face_up_cards):
                card_rect = self.get_card_rect(pile_index, card_index)
                if card_index == len(pile.face_up_cards) - 1:
                    visible_rect = card_rect  # 顶部牌全部可见
                else:
                    next_card_rect = self.get_card_rect(pile_index, card_index + 1)
                    visible_height = next_card_rect.y - card_rect.y
                    visible_rect = pygame.Rect(
                        card_rect.x,
                        card_rect.y,
                        card_rect.width,
                        visible_height
                    )
                if visible_rect.collidepoint(x, y):
                    return (pile_index, card_index)
        return None

    def draw_card(self, card: Card, x: int, y: int, scale: float = 1.0, selected: bool = False, face_up: bool = True):
        """绘制单张卡牌"""
        # 计算缩放后的尺寸
        scaled_width = int(self.card_width * scale)
        scaled_height = int(self.card_height * scale)
        
        # 计算缩放后的位置，保持卡牌左上角不变
        scaled_x = x
        scaled_y = y

        if not face_up:
            # 绘制卡牌背面
            pygame.draw.rect(self.screen, COLORS['BLUE'], (scaled_x, scaled_y, scaled_width, scaled_height))
            pygame.draw.rect(self.screen, COLORS['BLACK'], (scaled_x, scaled_y, scaled_width, scaled_height), 2)
            # 绘制背面花纹
            for i in range(0, scaled_width, 10):
                pygame.draw.line(self.screen, COLORS['LIGHT_BLUE'],
                               (scaled_x + i, scaled_y),
                               (scaled_x + i, scaled_y + scaled_height))
            return

        # 尝试加载卡牌图片
        card_image = self.assets.load_card_image(card.type, str(card.value))

        if card_image:
            if selected:
                pygame.draw.rect(self.screen, COLORS['YELLOW'],
                               (scaled_x - 5, scaled_y - 5, scaled_width + 10, scaled_height + 10))
            scaled_image = pygame.transform.scale(card_image, (scaled_width, scaled_height))
            self.screen.blit(scaled_image, (scaled_x, scaled_y))
        else:
            # 绘制卡牌正面
            color = CARD_COLORS.get(card.type, COLORS['WHITE'])
            if selected:
                pygame.draw.rect(self.screen, COLORS['YELLOW'],
                               (scaled_x - 5, scaled_y - 5, scaled_width + 10, scaled_height + 10))

            pygame.draw.rect(self.screen, color, (scaled_x, scaled_y, scaled_width, scaled_height))
            pygame.draw.rect(self.screen, COLORS['BLACK'], (scaled_x, scaled_y, scaled_width, scaled_height), 2)

            # 绘制卡牌数值（移到顶部）
            value_text = self.font.render(str(card.value), True, COLORS['BLACK'])
            value_text = pygame.transform.scale(value_text,
                                             (int(value_text.get_width() * scale), int(value_text.get_height() * scale)))
            value_rect = value_text.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + 25))
            self.screen.blit(value_text, value_rect)

            # 绘制卡牌类型（移到中间）
            type_text = self.small_font.render(card.type, True, COLORS['BLACK'])
            type_text = pygame.transform.scale(type_text,
                                            (int(type_text.get_width() * scale), int(type_text.get_height() * scale)))
            type_rect = type_text.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + scaled_height // 2))
            self.screen.blit(type_text, type_rect)

    def draw_pile(self, pile_index: int, pile):
        """绘制牌堆"""
        x = 50 + pile_index * (self.card_width + 30)  # 增加间距
        y = self.pile_area_y

        # 绘制牌堆剩余数量
        remaining_text = self.small_font.render(f"Remaining: {len(pile.cards)}", True, COLORS['BLACK'])
        remaining_rect = remaining_text.get_rect(center=(x + self.card_width//2, y - 20))
        self.screen.blit(remaining_text, remaining_rect)

        # 先绘制暗牌
        hidden_cards_count = len(pile.cards) - len(pile.face_up_cards)
        for i in range(hidden_cards_count):
            self.draw_card(None, x, y + i * 30, 1.0, face_up=False)

        # 从底部开始绘制明牌，确保顶部的牌在最上层
        for i in range(len(pile.face_up_cards)):
            if self.dragging and self.drag_card and self.drag_card[0] == pile_index:
                if i >= self.drag_card[1]:  # 跳过正在拖动的卡牌及其上方的卡牌
                    continue
            
            card = pile.face_up_cards[i]
            card_y = y + (hidden_cards_count + i) * 30
            
            # 如果是顶部的牌，位置靠下一些
            if i == len(pile.face_up_cards) - 1:
                card_y += 20
            
            # 设置缩放
            scale = self.hover_scale if self.hovered_card == (pile_index, i) else 1.0
            self.draw_card(card, x, card_y, scale, face_up=True)

    def draw_dragging_card(self):
        """绘制正在拖拽的卡牌"""
        if self.dragging and self.drag_card:
            pile_index, start_index = self.drag_card
            pile = self.game.piles[pile_index]
            
            # 计算要绘制的卡牌
            top_index = len(pile.face_up_cards) - 1
            cards_to_draw = pile.face_up_cards[start_index:top_index + 1]
            
            # 获取鼠标位置
            mouse_x, mouse_y = pygame.mouse.get_pos()
            base_x = mouse_x - self.drag_offset[0]
            base_y = mouse_y - self.drag_offset[1]
            
            # 绘制选中的卡牌组
            for i, card in enumerate(cards_to_draw):
                card_y = base_y + i * 30
                self.draw_card(card, base_x, card_y, self.hover_scale, True)

    def draw_bottom_area(self):
        """绘制底部区域"""
        # 绘制底部区域背景
        pygame.draw.rect(self.screen, COLORS['GRAY'], self.bottom_area_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], self.bottom_area_rect, 2)

        # 绘制结算区域
        pygame.draw.rect(self.screen, COLORS['WHITE'], self.settlement_area_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], self.settlement_area_rect, 2)
        
        # 绘制结算区域标题
        title_text = self.title_font.render("Settlement Area", True, COLORS['BLACK'])
        title_rect = title_text.get_rect(center=(self.settlement_area_rect.centerx, 
                                               self.settlement_area_rect.y + 25))
        self.screen.blit(title_text, title_rect)

        # 绘制生命值区域
        pygame.draw.rect(self.screen, COLORS['WHITE'], self.hp_area_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], self.hp_area_rect, 2)
        
        # 绘制生命值
        hp_text = self.title_font.render(f"HP: {self.game.player.hp}/{self.game.player.max_hp}", True, COLORS['BLACK'])
        hp_rect = hp_text.get_rect(center=self.hp_area_rect.center)
        self.screen.blit(hp_text, hp_rect)

        # 绘制遗物区域
        pygame.draw.rect(self.screen, COLORS['WHITE'], self.relic_area_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], self.relic_area_rect, 2)
        
        # 绘制遗物区域标题
        relic_title = self.title_font.render("Relics", True, COLORS['BLACK'])
        relic_title_rect = relic_title.get_rect(center=(self.relic_area_rect.centerx, 
                                                      self.relic_area_rect.y + 25))
        self.screen.blit(relic_title, relic_title_rect)
        
        # 绘制遗物
        relic_spacing = 90  # 增加间距
        for i, relic in enumerate(self.game.player.relics):
            relic_rect = pygame.Rect(
                self.relic_area_rect.x + 20 + i * relic_spacing,
                self.relic_area_rect.y + 70,  # 调整位置
                70,  # 增加尺寸
                70
            )
            # 绘制遗物图标
            pygame.draw.rect(self.screen, COLORS['YELLOW'], relic_rect)
            pygame.draw.rect(self.screen, COLORS['BLACK'], relic_rect, 2)
            
            # 绘制遗物名称
            relic_text = self.small_font.render(relic.name, True, COLORS['BLACK'])
            text_rect = relic_text.get_rect(center=(relic_rect.centerx, relic_rect.bottom + 15))
            self.screen.blit(relic_text, text_rect)
            
            # 绘制使用次数
            charges_text = self.tiny_font.render(f"Uses: {relic.charges}/{relic.max_charges}", True, COLORS['BLACK'])
            charges_rect = charges_text.get_rect(center=(relic_rect.centerx, relic_rect.bottom + 35))
            self.screen.blit(charges_text, charges_rect)

    def draw_settlement_area(self):
        """绘制结算区域"""
        # 绘制结算区域背景
        pygame.draw.rect(self.screen, COLORS['GRAY'], self.settlement_area_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], self.settlement_area_rect, 2)

        # 绘制标题
        title_text = self.font.render("结算区域", True, COLORS['BLACK'])
        title_rect = title_text.get_rect(center=(self.settlement_area_rect.centerx, 
                                               self.settlement_area_rect.top + 30))
        self.screen.blit(title_text, title_rect)

        # 绘制结算区域中的卡牌
        for i, card in enumerate(self.game.settlement_area):
            x = self.settlement_area_rect.x + 20 + (i % 2) * 120
            y = self.settlement_area_rect.y + 60 + (i // 2) * 160
            self.draw_card(card, x, y, 0.8)

        # 绘制结算统计信息
        summary = self.game.get_settlement_summary()
        y_offset = self.settlement_area_rect.bottom - 150
        
        # 攻击值
        attack_text = self.font.render(f"Attack: {summary['attack']}", True, COLORS['RED'])
        self.screen.blit(attack_text, (self.settlement_area_rect.x + 20, y_offset))
        
        # 防御值
        defense_text = self.font.render(f"Defense: {summary['defense']}", True, COLORS['BLUE'])
        self.screen.blit(defense_text, (self.settlement_area_rect.x + 20, y_offset + 40))
        
        # 治疗值
        heal_text = self.font.render(f"Heal: {summary['heal']}", True, COLORS['GREEN'])
        self.screen.blit(heal_text, (self.settlement_area_rect.x + 20, y_offset + 80))

        # 如果有诅咒卡，显示警告
        if summary['has_curse']:
            curse_text = self.font.render("Curse Active!", True, COLORS['RED'])
            self.screen.blit(curse_text, (self.settlement_area_rect.x + 20, y_offset + 120))

    def add_effect(self, effect_type: str, value: int, position: Tuple[int, int]):
        """添加视觉效果"""
        self.effects.append({
            'type': effect_type,
            'value': value,
            'position': position,
            'start_time': pygame.time.get_ticks(),
            'alpha': 255
        })

    def draw_effects(self):
        """绘制视觉效果"""
        current_time = pygame.time.get_ticks()
        new_effects = []
        
        for effect in self.effects:
            elapsed = current_time - effect['start_time']
            if elapsed < self.effect_duration:
                # 计算效果的透明度
                alpha = int(255 * (1 - elapsed / self.effect_duration))
                # 计算上升的位置
                y_offset = int(elapsed / self.effect_duration * 50)
                
                # 创建文本
                if effect['type'] == 'damage':
                    color = COLORS['RED']
                    text = f"-{effect['value']}"
                elif effect['type'] == 'heal':
                    color = COLORS['GREEN']
                    text = f"+{effect['value']}"
                elif effect['type'] == 'defense':
                    color = COLORS['BLUE']
                    text = f"+{effect['value']}"
                
                # 渲染文本
                text_surface = self.font.render(text, True, color)
                text_surface.set_alpha(alpha)
                
                # 绘制文本
                pos = (effect['position'][0], effect['position'][1] - y_offset)
                self.screen.blit(text_surface, pos)
                
                new_effects.append(effect)
        
        self.effects = new_effects

    def draw(self):
        """绘制整个游戏界面"""
        # 绘制背景
        self.screen.blit(self.background, (0, 0))

        # 绘制所有牌堆
        for i, pile in enumerate(self.game.piles):
            self.draw_pile(i, pile)

        # 绘制底部区域（包含生命值、遗物和结算区域）
        self.draw_bottom_area()

        # 绘制正在拖拽的卡牌
        self.draw_dragging_card()

        # 绘制视觉效果
        self.draw_effects()

        pygame.display.flip()

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """处理鼠标移动事件"""
        # 更新悬停的卡牌
        self.hovered_card = self.get_card_at_pos(pos)

    def handle_mouse_down(self, pos: Tuple[int, int]):
        """处理鼠标按下事件"""
        # 从顶部开始检查卡牌，这样可以优先选择上层的卡牌
        for pile_index, pile in enumerate(self.game.piles):
            for card_index in range(len(pile.face_up_cards) - 1, -1, -1):
                card_rect = self.get_card_rect(pile_index, card_index)
                if card_rect.collidepoint(pos):
                    # 只允许拖动顶部卡牌或其下最多4张卡牌
                    top_card_index = len(pile.face_up_cards) - 1
                    if card_index >= top_card_index - 4:
                        self.dragging = True
                        self.drag_card = (pile_index, card_index)
                        self.drag_start_pos = pos
                        self.drag_offset = (pos[0] - card_rect.x, pos[1] - card_rect.y)
                        return
                    break  # 如果点击的是更下面的卡牌，直接退出

    def handle_mouse_up(self, pos: Tuple[int, int]):
        """处理鼠标释放事件"""
        if self.dragging and self.drag_card:
            # 检查是否可以放置到结算区域
            if self.settlement_area_rect.collidepoint(pos):
                from_pile, from_index = self.drag_card
                pile = self.game.piles[from_pile]
                
                # 获取要结算的所有卡牌
                cards_to_settle = pile.face_up_cards[from_index:]
                
                # 处理结算
                success, message = self.game.add_to_settlement(list(cards_to_settle))
                if success:
                    # 添加视觉效果
                    effect_pos = pos
                    for card in cards_to_settle:
                        if card.type == 'attack':
                            self.add_effect('damage', card.value, effect_pos)
                        elif card.type in ['defense', 'heal']:
                            self.add_effect('heal', card.value, effect_pos)
                        effect_pos = (effect_pos[0], effect_pos[1] + 30)
                    
                    # 移除所有结算的卡牌
                    for card in cards_to_settle:
                        pile.remove_card(pile.cards.index(card))
                    
                    # 如果牌堆还有卡牌，翻开顶部卡牌
                    if pile.cards and not pile.face_up_cards:
                        pile.flip_top_card()
            
            # 重置拖动状态
            self.dragging = False
            self.drag_card = None
            self.drag_offset = (0, 0)

    def handle_events(self):
        """处理所有游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    # 检查是否点击了遗物
                    mouse_pos = event.pos
                    for i, relic in enumerate(self.game.player.relics):
                        relic_rect = pygame.Rect(
                            self.relic_area_rect.x + 20 + i * 80,
                            self.relic_area_rect.y + 60,  # 更新遗物位置
                            60,
                            60
                        )
                        if relic_rect.collidepoint(mouse_pos):
                            # 触发遗物效果
                            if relic.trigger_type == 'click':
                                success, message = relic.trigger()
                            return True

                    # 检查卡牌点击
                    for pile_index, pile in enumerate(self.game.piles):
                        if len(pile.face_up_cards) == 0:
                            continue
                            
                        # 获取牌堆中可以拖动的卡牌范围
                        top_index = len(pile.face_up_cards) - 1
                        start_index = max(0, top_index - 4)  # 最多可以拖动5张牌
                        
                        # 检查从顶部开始的每张牌
                        for card_index in range(top_index, start_index - 1, -1):
                            card_rect = self.get_card_rect(pile_index, card_index)
                            if card_rect.collidepoint(event.pos):
                                self.dragging = True
                                self.drag_card = (pile_index, card_index)
                                self.drag_offset = (event.pos[0] - card_rect.x, event.pos[1] - card_rect.y)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging:
                    # 检查是否可以放置到结算区域
                    if self.settlement_area_rect.collidepoint(event.pos):
                        from_pile, from_index = self.drag_card
                        pile = self.game.piles[from_pile]
                        
                        # 获取要结算的所有卡牌
                        cards_to_settle = pile.face_up_cards[from_index:]
                        
                        # 处理结算
                        success, message = self.game.add_to_settlement(list(cards_to_settle))
                        if success:
                            # 移除所有结算的卡牌
                            for card in cards_to_settle:
                                pile.remove_card(pile.cards.index(card))
                            
                            # 如果牌堆还有卡牌，翻开顶部卡牌
                            if pile.cards and not pile.face_up_cards:
                                pile.flip_top_card()
                    else:
                        # 检查是否可以放置到其他牌堆
                        for pile_index, pile in enumerate(self.game.piles):
                            pile_rect = pygame.Rect(
                                50 + pile_index * (self.card_width + 20),
                                self.pile_area_y,  # 更新牌堆位置
                                self.card_width,
                                self.card_height * 3
                            )
                            if pile_rect.collidepoint(event.pos):
                                from_pile, from_index = self.drag_card
                                if from_pile != pile_index:
                                    success, message = self.game.move_cards(from_pile, pile_index, from_index)
            
                    # 重置拖动状态
                    self.dragging = False
                    self.drag_card = None
                    self.drag_offset = (0, 0)
            
            elif event.type == pygame.MOUSEMOTION:
                if not self.dragging:
                    mouse_pos = event.pos
                    self.hovered_card = None
                    # 检查遗物悬停
                    for i, relic in enumerate(self.game.player.relics):
                        relic_rect = pygame.Rect(
                            self.relic_area_rect.x + 20 + i * 80,
                            self.relic_area_rect.y + 60,  # 更新遗物位置
                            60,
                            60
                        )
                        if relic_rect.collidepoint(mouse_pos):
                            return True

                    # 检查卡牌悬停（只在未被遮挡区域才算悬停）
                    self.hovered_card = self.get_card_at_pos(mouse_pos)
        
        return True

    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)

            # 检查游戏状态
            if self.game.check_game_over():
                print("游戏结束！")
                running = False
            elif self.game.check_win_condition():
                print("恭喜获胜！")
                running = False

        pygame.quit()
        sys.exit()