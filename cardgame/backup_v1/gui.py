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

        # 拖拽相关
        self.dragging = False
        self.drag_card = None
        self.drag_start_pos = None
        self.drag_offset = (0, 0)
        self.hovered_card = None

        # 游戏阶段
        self.game_phase = "Preparation Phase"

        # 结算区域
        self.settlement_area_rect = pygame.Rect(
            self.screen_width - 300,  # 右侧
            200,  # 与牌堆对齐
            250,  # 宽度
            400   # 高度
        )

        # 初始化界面
        self.initialize_gui()

        # 新增：卡牌GUI对象列表
        self.card_guis = []
        self.update_card_guis()

    def initialize_gui(self):
        """初始化GUI元素"""
        # 尝试加载背景图片
        self.background = self.assets.load_background('main_bg')
        if not self.background:
            # 如果没有背景图片，使用纯色背景
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill(COLORS['LIGHT_BLUE'])

        # 加载UI元素
        self.hp_bar = self.assets.load_ui_element('hp_bar')
        self.relic_frame = self.assets.load_ui_element('relic_frame')
        self.card_frame = self.assets.load_ui_element('card_frame')

    def get_card_rect(self, pile_index: int, card_index: int) -> pygame.Rect:
        """获取卡牌在屏幕上的矩形区域"""
        x = 50 + pile_index * (self.card_width + 20)
        base_y = 200
        
        # 计算暗牌数量
        pile = self.game.piles[pile_index]
        hidden_cards_count = len(pile.cards) - len(pile.face_up_cards)
        
        # 计算卡牌位置
        y = base_y + (hidden_cards_count + card_index) * 30
        if card_index == len(pile.face_up_cards) - 1:  # 如果是顶部的牌
            y += 20  # 位置靠下一些
            
        return pygame.Rect(x, y, self.card_width, self.card_height)

    def get_card_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """获取指定位置的卡牌"""
        x, y = pos
        for pile_index, pile in enumerate(self.game.piles):
            for card_index, _ in enumerate(pile.face_up_cards):
                card_rect = self.get_card_rect(pile_index, card_index)
                if card_rect.collidepoint(x, y):
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
            value_rect = value_text.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + 20))
            self.screen.blit(value_text, value_rect)

            # 绘制卡牌类型（移到中间）
            type_text = self.font.render(card.type, True, COLORS['BLACK'])
            type_text = pygame.transform.scale(type_text,
                                            (int(type_text.get_width() * scale), int(type_text.get_height() * scale)))
            type_rect = type_text.get_rect(center=(scaled_x + scaled_width // 2, scaled_y + scaled_height // 2))
            self.screen.blit(type_text, type_rect)

    def draw_pile(self, pile_index: int, pile):
        """绘制牌堆"""
        x = 50 + pile_index * (self.card_width + 20)
        y = 200

        # 绘制牌堆剩余数量
        remaining_text = self.small_font.render(f"Remaining: {len(pile.cards)}", True, COLORS['BLACK'])
        self.screen.blit(remaining_text, (x, y - 30))

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

    def draw_game_phase(self):
        """绘制游戏阶段"""
        phase_text = self.title_font.render(f"Phase: {self.game_phase}", True, COLORS['BLACK'])
        phase_rect = phase_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(phase_text, phase_rect)

        # 根据游戏状态更新阶段
        if self.game.active_curse:
            if not self.game.defense_cards:
                self.game_phase = "Defense Phase"
            elif not self.game.attack_cards:
                self.game_phase = "Attack Phase"
            else:
                self.game_phase = "Battle Phase"
        else:
            self.game_phase = "Preparation Phase"

    def draw_player_info(self):
        """绘制玩家信息"""
        # 生命值
        if self.hp_bar:
            hp_ratio = self.game.player.hp / self.game.player.max_hp
            hp_width = int(200 * hp_ratio)
            hp_rect = self.hp_bar.get_rect()
            hp_rect.topleft = (20, 20)
            self.screen.blit(self.hp_bar, hp_rect)
            pygame.draw.rect(self.screen, COLORS['RED'], (20, 20, hp_width, hp_rect.height))
        else:
            hp_text = self.font.render(f"HP: {self.game.player.hp}/{self.game.player.max_hp}",
                                       True, COLORS['BLACK'])
            self.screen.blit(hp_text, (20, 20))

        # 显示当前诅咒卡状态
        if self.game.active_curse:
            curse_card, curse_value = self.game.active_curse
            curse_text = self.font.render(f"Curse: {curse_card.type}({curse_value})", True, COLORS['BLACK'])
            self.screen.blit(curse_text, (20, 60))

            # 显示防御值
            defense_value = sum(card.value for card in self.game.defense_cards)
            defense_text = self.font.render(f"Defense: {defense_value}/{curse_value}", True, COLORS['BLUE'])
            self.screen.blit(defense_text, (20, 100))

            # 显示攻击值
            attack_value = sum(card.value for card in self.game.attack_cards)
            attack_text = self.font.render(f"Attack: {attack_value}/{curse_value}", True, COLORS['RED'])
            self.screen.blit(attack_text, (20, 140))

            # 绘制进度条
            bar_width = 200
            bar_height = 20
            bar_x = 20
            bar_y = 180

            # 防御进度条
            defense_ratio = min(1.0, defense_value / curse_value)
            pygame.draw.rect(self.screen, COLORS['GRAY'], (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, COLORS['BLUE'],
                             (bar_x, bar_y, int(bar_width * defense_ratio), bar_height))

            # 攻击进度条
            attack_ratio = min(1.0, attack_value / curse_value)
            pygame.draw.rect(self.screen, COLORS['GRAY'], (bar_x, bar_y + 30, bar_width, bar_height))
            pygame.draw.rect(self.screen, COLORS['RED'],
                             (bar_x, bar_y + 30, int(bar_width * attack_ratio), bar_height))

        # 显示遗物
        if self.relic_frame:
            for i, relic in enumerate(self.game.player.relics):
                relic_image = self.assets.load_ui_element(f"relic_{relic}")
                if relic_image:
                    self.screen.blit(relic_image, (100 + i * 60, 240))
                    self.screen.blit(self.relic_frame, (95 + i * 60, 235))
        else:
            relics_text = self.font.render("Relics:", True, COLORS['BLACK'])
            self.screen.blit(relics_text, (20, 240))
            for i, relic in enumerate(self.game.player.relics):
                relic_text = self.small_font.render(relic, True, COLORS['BLACK'])
                self.screen.blit(relic_text, (100, 240 + i * 25))

    def update_card_guis(self):
        self.card_guis = []
        # 创建卡牌GUI对象
        for i, card in enumerate(self.game.player.hand):
            # 计算卡牌位置，牌顶的牌位置靠下
            x = 100 + i * 120
            y = 400 if i == len(self.game.player.hand) - 1 else 380
            card_gui = CardGUI(card, x, y)
            self.card_guis.append(card_gui)
        
        # 设置牌顶的牌和上面的牌
        for i, card_gui in enumerate(self.card_guis):
            if i == len(self.card_guis) - 1:
                card_gui.is_top_card = True
            else:
                # 将非牌顶的牌添加到上面牌的cards_above列表中
                self.card_guis[i + 1].cards_above.append(card_gui)
                # 限制最多5张牌
                if len(self.card_guis[i + 1].cards_above) > 5:
                    self.card_guis[i + 1].cards_above.pop(0)

    def draw_settlement_area(self):
        """绘制结算区域"""
        # 绘制结算区域背景
        pygame.draw.rect(self.screen, COLORS['GRAY'], self.settlement_area_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], self.settlement_area_rect, 2)

        # 绘制标题
        title_text = self.font.render("Settlement Area", True, COLORS['BLACK'])
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

    def draw(self):
        """绘制整个游戏界面"""
        # 绘制背景
        self.screen.blit(self.background, (0, 0))

        # 绘制游戏阶段
        self.draw_game_phase()

        # 绘制玩家信息
        self.draw_player_info()

        # 绘制所有牌堆
        for i, pile in enumerate(self.game.piles):
            self.draw_pile(i, pile)

        # 绘制结算区域
        self.draw_settlement_area()

        # 绘制正在拖拽的卡牌
        self.draw_dragging_card()

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
                success, message = self.game.add_to_settlement(list(cards_to_settle))  # 确保是列表
                if success:
                    # 移除所有结算的卡牌
                    for card in cards_to_settle:
                        pile.remove_card(pile.cards.index(card))
                    
                    # 如果牌堆还有卡牌，翻开顶部卡牌
                    if pile.cards and not pile.face_up_cards:
                        pile.flip_top_card()
                    
                    print(message)
            else:
                # 检查是否可以放置到其他牌堆
                for pile_index, pile in enumerate(self.game.piles):
                    pile_rect = pygame.Rect(
                        50 + pile_index * (self.card_width + 20),
                        200,
                        self.card_width,
                        self.card_height * 3
                    )
                    if pile_rect.collidepoint(pos):
                        from_pile, from_index = self.drag_card
                        if from_pile != pile_index:
                            success, message = self.game.move_cards(from_pile, pile_index, from_index)
                            if not success:
                                print("Cannot move: Can only move to piles with higher values")
                            else:
                                print(message)
            
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
                    # 从顶部开始检查卡牌，这样可以优先选择上层的卡牌
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
                                return True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging:
                    # 检查是否可以放置到结算区域
                    if self.settlement_area_rect.collidepoint(event.pos):
                        from_pile, from_index = self.drag_card
                        pile = self.game.piles[from_pile]
                        
                        # 获取要结算的所有卡牌
                        cards_to_settle = pile.face_up_cards[from_index:]
                        
                        # 处理结算
                        success, message = self.game.add_to_settlement(list(cards_to_settle))  # 确保是列表
                        if success:
                            # 移除所有结算的卡牌
                            for card in cards_to_settle:
                                pile.remove_card(pile.cards.index(card))
                            
                            # 如果牌堆还有卡牌，翻开顶部卡牌
                            if pile.cards and not pile.face_up_cards:
                                pile.flip_top_card()
                            
                            print(message)
                    else:
                        # 检查是否可以放置到其他牌堆
                        for pile_index, pile in enumerate(self.game.piles):
                            pile_rect = pygame.Rect(
                                50 + pile_index * (self.card_width + 20),
                                200,
                                self.card_width,
                                self.card_height * 3
                            )
                            if pile_rect.collidepoint(event.pos):
                                from_pile, from_index = self.drag_card
                                if from_pile != pile_index:
                                    success, message = self.game.move_cards(from_pile, pile_index, from_index)
                                    if not success:
                                        print("Cannot move: Can only move to piles with higher values")
                                    else:
                                        print(message)
                    
                    # 重置拖动状态
                    self.dragging = False
                    self.drag_card = None
                    self.drag_offset = (0, 0)
            
            elif event.type == pygame.MOUSEMOTION:
                if not self.dragging:
                    mouse_pos = event.pos
                    self.hovered_card = None
                    for pile_index, pile in enumerate(self.game.piles):
                        for card_index in range(len(pile.face_up_cards)):
                            card_rect = self.get_card_rect(pile_index, card_index)
                            if card_rect.collidepoint(mouse_pos):
                                self.hovered_card = (pile_index, card_index)
                                break
        
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