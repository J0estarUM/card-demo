import pygame
import sys
import os
import time
import math
from config import *
from typing import Tuple, Optional, Dict
from game import Game
from card import Card
from config import UI_IMAGES, BLOOD_MOVE_RANGE, HEAD_MOVE_X, HEAD_MOVE_Y
from rule.difficulty import DifficultyMenu
from rule.modal_popup import ModalPopup


# 资源管理类
class AssetManager:
    def __init__(self):
        self.images: Dict[str, pygame.Surface] = {}
        self.card_images: Dict[str, Dict[str, pygame.Surface]] = {}
        self.ui_elements: Dict[str, pygame.Surface] = {}
        self.backgrounds: Dict[str, pygame.Surface] = {}
        self.modal_popup: Optional[ModalPopup] = None

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
    def __init__(self, game: Game, difficulty=None, modal_popup=None):
        pygame.init()
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Card Game")
        self.clock = pygame.time.Clock()
        # 难度相关
        self.difficulty = difficulty
        self.move_limit = 3
        self.move_count = 0
        self.last_turn = 0
        # 初始化资源管理器
        self.assets = AssetManager()
        self.assets.modal_popup = modal_popup

        # 卡牌尺寸
        self.card_width = card_width
        self.card_height = card_height
        self.card_scale = card_scale
        self.hover_scale = hover_scale

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
        self.bottom_area_height = bottom_area_height
        self.bottom_area_rect = pygame.Rect(
            0,
            self.screen_height - self.bottom_area_height,
            self.screen_width,
            self.bottom_area_height
        )

        # 结算区域（左侧）
        self.settlement_area_rect = pygame.Rect(
            settlement_area_x,
            settlement_area_y,
            settlement_area_width,
            settlement_area_height
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
        self.pile_area_y = int(pile_area_y * SCALE)

        # 视觉效果
        self.effects = []
        self.effect_duration = effect_duration  # 效果持续时间（毫秒）
        
        # 结算区相关
        self.settlement_display_timer = 0
        self.settlement_display_cards = []
        self.settlement_display_from_pile = None
        
        # 初始化界面
        self.initialize_gui()

    def initialize_gui(self):
        """初始化GUI资源"""
        # 加载背景
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(COLORS['WHITE'])

        # 加载UI图片（批量加载，修正path获取方式）
        self.ui_images = {}
        for key, info in UI_IMAGES.items():
            path = info["path"]
            try:
                img = pygame.image.load(path).convert_alpha()
                self.ui_images[key] = img
            except Exception as e:
                print(f"加载UI图片失败: {key} - {path}，错误：{e}")
                self.ui_images[key] = None

        # 加载卡牌背面
        self.card_back_img = pygame.image.load(back_card).convert_alpha()
        self.card_back_img = pygame.transform.scale(self.card_back_img, (self.card_width, self.card_height))

        # 加载正面卡牌
        self.attack_img = pygame.image.load(attack_card).convert_alpha()
        self.defense_img = pygame.image.load(defense_card).convert_alpha()
        self.curse_img = pygame.image.load(curse_card).convert_alpha()
        self.heal_img = pygame.image.load(heal_card).convert_alpha()
        self.attack_img = pygame.transform.scale(
            pygame.image.load(attack_card).convert_alpha(), (self.card_width, self.card_height))
        self.defense_img = pygame.transform.scale(
            pygame.image.load(defense_card).convert_alpha(), (self.card_width, self.card_height))
        self.curse_img = pygame.transform.scale(
            pygame.image.load(curse_card).convert_alpha(), (self.card_width, self.card_height))
        self.heal_img = pygame.transform.scale(
            pygame.image.load(heal_card).convert_alpha(), (self.card_width, self.card_height))

        # 加载生命值条
        self.hp_bar = pygame.Surface((0,0))
        self.hp_bar.fill(COLORS['GRAY'])

        # 加载遗物框
        self.relic_frame = pygame.Surface((50, 50))
        self.relic_frame.fill(COLORS['YELLOW'])
        pygame.draw.rect(self.relic_frame, COLORS['BLACK'], self.relic_frame.get_rect(), 2)

        # 加载数值图片
        self.num_images = {}
        for value, path in NUM_IMAGES.items():
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (30, 30))  # 可根据需要调整尺寸
            self.num_images[value] = img

    def get_card_rect(self, pile_index: int, card_index: int, margin: int = 10) -> pygame.Rect:
        x = pile_start_x + pile_index * (self.card_width + card_spacing)
        base_y = self.pile_area_y
        pile = self.game.piles[pile_index]
        hidden_cards_count = len(pile.cards) - len(pile.face_up_cards)
        y = base_y + (hidden_cards_count + card_index) * card_spacing
        return pygame.Rect(x + margin, y + margin, self.card_width - 2 * margin, self.card_height - 2 * margin)

    def select_card_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        返回鼠标位置选中的牌（pile_index, card_index），只允许选中可见区域。
        优先级：最上层优先。
        """
        x, y = pos
        for pile_index, pile in enumerate(self.game.piles):
            n = len(pile.face_up_cards)
            if n == 0:
                continue
            for card_index in reversed(range(n)):
                card_rect = self.get_card_rect(pile_index, card_index, margin=card_select_margin)
                if card_index == n - 1:
                    if card_rect.collidepoint(x, y):
                        return (pile_index, card_index)
                else:
                    next_card_rect = self.get_card_rect(pile_index, card_index + 1, margin=card_select_margin)
                    visible_height = next_card_rect.y - card_rect.y
                    if visible_height > 0:
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
        width = int(self.card_width * scale)
        height = int(self.card_height * scale)
        
        # 计算缩放后的位置，保持卡牌左上角不变
        scaled_x = x
        scaled_y = y
        if face_up:
            if card.type == 'attack':
                self.screen.blit(self.attack_img, (scaled_x, scaled_y))
                # 绘制数值图片
                num_img = self.num_images.get(card.value)
                if num_img:
                    offset_x, offset_y = NUM_IMAGE_OFFSET
                    num_scale = NUM_IMAGE_SCALE * scale
                    scaled_num_width = int(num_img.get_width() * num_scale)
                    scaled_num_height = int(num_img.get_height() * num_scale)
                    scaled_num_img = pygame.transform.smoothscale(num_img, (scaled_num_width, scaled_num_height))
                    num_x = scaled_x + (width - scaled_num_width) // 2 + int(offset_x * scale)
                    num_y = scaled_y + int(offset_y * scale)
                    self.screen.blit(scaled_num_img, (num_x, num_y))
                return
            elif card.type == 'defense':
                self.screen.blit(self.defense_img, (scaled_x, scaled_y))
                num_img = self.num_images.get(card.value)
                if num_img:
                    offset_x, offset_y = NUM_IMAGE_OFFSET
                    num_scale = NUM_IMAGE_SCALE * scale
                    scaled_num_width = int(num_img.get_width() * num_scale)
                    scaled_num_height = int(num_img.get_height() * num_scale)
                    scaled_num_img = pygame.transform.smoothscale(num_img, (scaled_num_width, scaled_num_height))
                    num_x = scaled_x + (width - scaled_num_width) // 2 + int(offset_x * scale)
                    num_y = scaled_y + int(offset_y * scale)
                    self.screen.blit(scaled_num_img, (num_x, num_y))
                return
            elif card.type == 'curse':
                self.screen.blit(self.curse_img, (scaled_x, scaled_y))
                num_img = self.num_images.get(card.value)
                if num_img:
                    offset_x, offset_y = NUM_IMAGE_OFFSET
                    num_scale = NUM_IMAGE_SCALE * scale
                    scaled_num_width = int(num_img.get_width() * num_scale)
                    scaled_num_height = int(num_img.get_height() * num_scale)
                    scaled_num_img = pygame.transform.smoothscale(num_img, (scaled_num_width, scaled_num_height))
                    num_x = scaled_x + (width - scaled_num_width) // 2 + int(offset_x * scale)
                    num_y = scaled_y + int(offset_y * scale)
                    self.screen.blit(scaled_num_img, (num_x, num_y))
                return
            elif card.type == 'heal':
                self.screen.blit(self.heal_img, (scaled_x, scaled_y))
                num_img = self.num_images.get(card.value)
                if num_img:
                    offset_x, offset_y = NUM_IMAGE_OFFSET
                    num_scale = NUM_IMAGE_SCALE * scale
                    scaled_num_width = int(num_img.get_width() * num_scale)
                    scaled_num_height = int(num_img.get_height() * num_scale)
                    scaled_num_img = pygame.transform.smoothscale(num_img, (scaled_num_width, scaled_num_height))
                    num_x = scaled_x + (width - scaled_num_width) // 2 + int(offset_x * scale)
                    num_y = scaled_y + int(offset_y * scale)
                    self.screen.blit(scaled_num_img, (num_x, num_y))
                return

        if not face_up:
            if not face_up:
                # 绘制卡牌背面图片
                self.screen.blit(self.card_back_img, (scaled_x, scaled_y))
                return
            return

    def draw_pile(self, pile_index: int, pile):
        """绘制牌堆"""
        x = pile_start_x + pile_index * (self.card_width + card_spacing)  # 增加间距
        y = self.pile_area_y

        # 绘制牌堆剩余数量
        remaining_text = self.small_font.render(f"Remaining: {len(pile.cards)}", True, COLORS['BLACK'])
        remaining_rect = remaining_text.get_rect(center=(x + self.card_width//2, y - 20))
        self.screen.blit(remaining_text, remaining_rect)

        # 先绘制暗牌
        hidden_cards_count = len(pile.cards) - len(pile.face_up_cards)
        for i in range(hidden_cards_count):
            self.draw_card(None, x, y + i * card_spacing, 1.0, face_up=False)

        # 从底部开始绘制明牌，确保顶部的牌在最上层
        for i in range(len(pile.face_up_cards)):
            # 拖动时跳过正在拖动的牌及其上方的牌
            if self.dragging and self.drag_card and self.drag_card[0] == pile_index:
                if i >= self.drag_card[1]:
                    continue
            card = pile.face_up_cards[i]
            card_y = y + (hidden_cards_count + i) * card_spacing
            self.draw_card(card, x, card_y, 1.0, face_up=True)

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
                card_y = base_y + i * card_spacing
                self.draw_card(card, base_x, card_y, self.hover_scale, True)

    def draw_bottom_area(self):
        """底部区域不再绘制任何内容"""
        pass

    def draw_settlement_area(self):
        """绘制结算区域"""
        # 不再绘制结算区背景和标题，直接绘制结算区卡牌
        if self.settlement_display_cards:
            # 统计各类型总和
            type_sums = {'attack': 0, 'defense': 0, 'curse': 0, 'heal': 0}
            for card in self.settlement_display_cards:
                if card.type in type_sums:
                    type_sums[card.type] += card.value
            color_map = {'attack': (220,20,60), 'defense': (30,144,255), 'curse': (0,0,0), 'heal': (0,180,0)}
            # 计算展示区所有卡牌的中心x和最上方y
            xs = []
            ys = []
            for i, card in enumerate(self.settlement_display_cards):
                x = self.settlement_area_rect.x + SETTLEMENT_DISPLAY_OFFSET[0] + (i % SETTLEMENT_DISPLAY_COLS) * SETTLEMENT_DISPLAY_X_SPACING
                y = self.settlement_area_rect.y + SETTLEMENT_DISPLAY_OFFSET[1] + (i // SETTLEMENT_DISPLAY_COLS) * SETTLEMENT_DISPLAY_Y_SPACING
                xs.append(x + int(self.card_width * SETTLEMENT_DISPLAY_SCALE)//2)
                ys.append(y)
            center_x = sum(xs)//len(xs)
            min_y = min(ys)
            # 构造所有有数值的类型的文本surface
            value_font = pygame.font.SysFont(None, 40)
            texts = []
            for t in ['attack','defense','curse','heal']:
                if type_sums[t] > 0:
                    value_text = str(type_sums[t])
                    text_surface = value_font.render(value_text, True, color_map[t])
                    outline_text = value_font.render(value_text, True, (255,255,255))
                    texts.append((text_surface, outline_text, t))
            # 横向排列，整体居中
            total_width = sum(s.get_width() for s,_,_ in texts) + (len(texts)-1)*20
            start_x = center_x - total_width//2
            for idx, (text_surface, outline_text, t) in enumerate(texts):
                text_x = start_x
                text_y = min_y - 32
                text_rect = text_surface.get_rect()
                text_rect.topleft = (text_x, text_y)
                outline_rect = outline_text.get_rect(topleft=(text_x, text_y))
                # 白色描边
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if dx != 0 or dy != 0:
                            outline_rect2 = outline_rect.copy()
                            outline_rect2.x += dx
                            outline_rect2.y += dy
                            self.screen.blit(outline_text, outline_rect2)
                self.screen.blit(text_surface, text_rect)
                start_x += text_surface.get_width() + 20
            # 继续绘制卡牌
            for i, card in enumerate(self.settlement_display_cards):
                x = self.settlement_area_rect.x + SETTLEMENT_DISPLAY_OFFSET[0] + (i % SETTLEMENT_DISPLAY_COLS) * SETTLEMENT_DISPLAY_X_SPACING
                y = self.settlement_area_rect.y + SETTLEMENT_DISPLAY_OFFSET[1] + (i // SETTLEMENT_DISPLAY_COLS) * SETTLEMENT_DISPLAY_Y_SPACING
                self.draw_card(card, x, y, SETTLEMENT_DISPLAY_SCALE)
            # 展示时立即移除牌堆中的卡牌
            if self.settlement_display_timer > 0 and not hasattr(self, '_settlement_removed'):
                from_pile, from_index = self.settlement_display_from_pile
                pile = self.game.piles[from_pile]
                for card in self.settlement_display_cards:
                    if card in pile.cards:
                        pile.remove_card(pile.cards.index(card))
                self._settlement_removed = True
            # 到时后结算
            if time.time() - self.settlement_display_timer > SETTLEMENT_DISPLAY_DURATION:
                from_pile, from_index = self.settlement_display_from_pile
                pile = self.game.piles[from_pile]
                self.game.add_to_settlement(self.settlement_display_cards)
                # 结算后自动翻开顶部暗牌
                if pile.cards and not pile.face_up_cards:
                    pile.flip_top_card()
                # 结算后重置移动次数（新回合）
                self.move_count = 0
                self.last_turn += 1
                self.settlement_display_cards = []
                self.settlement_display_timer = 0
                if hasattr(self, '_settlement_removed'):
                    del self._settlement_removed
        else:
            for i, card in enumerate(self.game.settlement_area):
                x = self.settlement_area_rect.x + SETTLEMENT_DISPLAY_OFFSET[0] + (i % SETTLEMENT_DISPLAY_COLS) * SETTLEMENT_DISPLAY_X_SPACING
                y = self.settlement_area_rect.y + SETTLEMENT_DISPLAY_OFFSET[1] + (i // SETTLEMENT_DISPLAY_COLS) * SETTLEMENT_DISPLAY_Y_SPACING
                self.draw_card(card, x, y, SETTLEMENT_DISPLAY_SCALE)

    def add_effect(self, effect_type: str, value: int, position: Tuple[int, int]):
        """添加视觉效果"""
        self.effects.append({
            'type': effect_type,
            'value': value,
            'position': position,
            'start_time': pygame.time.get_ticks(),
            'alpha': 255
        })

    def draw(self):
        """绘制整个游戏界面"""
        # 1. 绘制背景和UI图片
        if self.ui_images.get("background"):
            self.screen.blit(self.ui_images["background"], (0, 0))
        else:
            self.screen.blit(self.background, (0, 0))
        for key, info in UI_IMAGES.items():
            if key in ("background", "blood", "bottleBack", "bottlefront"):
                continue
            img = self.ui_images.get(key)
            if img:
                pos = list(info.get("pos", (0, 0)))
                scale = info.get("scale", 1.0)
                # headL和headR动态运动
                if key in ("headL", "headR"):
                    t = pygame.time.get_ticks() / 1000.0
                    if key == "headL":
                        dx = int(HEAD_MOVE_X * math.sin(t))
                        dy = int(HEAD_MOVE_Y * math.cos(t))
                    else:
                        dx = int(HEAD_MOVE_X * math.sin(t + math.pi))
                        dy = int(HEAD_MOVE_Y * math.cos(t + math.pi))
                    pos[0] += dx
                    pos[1] += dy
                if scale != 1.0:
                    w, h = img.get_width(), img.get_height()
                    img = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
                self.screen.blit(img, pos)
        if "bottleBack" in self.ui_images and self.ui_images["bottleBack"]:
            info = UI_IMAGES["bottleBack"]
            img = self.ui_images["bottleBack"]
            pos = info.get("pos", (0, 0))
            scale = info.get("scale", 1.0)
            if scale != 1.0:
                w, h = img.get_width(), img.get_height()
                img = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
            self.screen.blit(img, pos)
        if "blood" in self.ui_images and self.ui_images["blood"]:
            blood_img = self.ui_images["blood"]
            info = UI_IMAGES["blood"]
            base_x, base_y = info["pos"]
            scale = info.get("scale", 1.0)
            if scale != 1.0:
                w, h = blood_img.get_width(), blood_img.get_height()
                blood_img = pygame.transform.smoothscale(blood_img, (int(w*scale), int(h*scale)))
            hp = self.game.player.hp
            max_hp = self.game.player.max_hp
            move_offset = int((1 - hp / max_hp) * BLOOD_MOVE_RANGE)
            blood_rect = blood_img.get_rect()
            blood_rect.topleft = (base_x, base_y + move_offset)
            self.screen.blit(blood_img, blood_rect)
        if "bottlefront" in self.ui_images and self.ui_images["bottlefront"]:
            info = UI_IMAGES["bottlefront"]
            img = self.ui_images["bottlefront"]
            pos = info.get("pos", (0, 0))
            scale = info.get("scale", 1.0)
            if scale != 1.0:
                w, h = img.get_width(), img.get_height()
                img = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
            self.screen.blit(img, pos)
        if "front" in self.ui_images and self.ui_images["front"]:
            info = UI_IMAGES["front"]
            img = self.ui_images["front"]
            pos = info.get("pos", (0, 0))
            scale = info.get("scale", 1.0)
            if scale != 1.0:
                w, h = img.get_width(), img.get_height()
                img = pygame.transform.smoothscale(img, (int(w*scale), int(h*scale)))
            self.screen.blit(img, pos)
        # 2. 绘制所有牌堆
        for i, pile in enumerate(self.game.piles):
            self.draw_pile(i, pile)
        # 3. 绘制结算区展示卡牌（延时后自动结算）
        self.draw_settlement_area()
        # 4. 绘制正在拖拽的卡牌
        self.draw_dragging_card()
        # 5. 绘制生命值数值（左下角）
        hp_font = pygame.font.SysFont(None, HP_FONT_SIZE)
        hp_text = hp_font.render(f"HP: {self.game.player.hp}/{self.game.player.max_hp}", True, HP_COLOR)
        self.screen.blit(hp_text, HP_POS)
        # 显示全局诅咒牌数值总和（屏幕顶部中央）
        curse_total = self.game.get_total_curse_value()
        curse_font = pygame.font.SysFont(None, 36)
        curse_text = curse_font.render(f"curse total: {curse_total}", True, (128, 0, 128))
        curse_rect = curse_text.get_rect(center=(self.screen_width-100, 30))
        self.screen.blit(curse_text, curse_rect)
        # 难度为1时显示剩余安全移动次数
        if self.difficulty == 1:
            safe_moves_left = max(0, self.move_limit - self.move_count)
            font = pygame.font.SysFont(None, 32)
            text = font.render(f"step: {safe_moves_left}", True, (30, 144, 255))
            text_rect = text.get_rect(bottomright=(self.screen_width - 40, self.screen_height - 40))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """处理鼠标移动事件"""
        self.hovered_card = self.select_card_at_pos(pos)

    def handle_mouse_down(self, pos: Tuple[int, int]):
        """处理鼠标按下事件"""
        result = self.select_card_at_pos(pos)
        if result is not None:
            pile_index, card_index = result
            pile = self.game.piles[pile_index]
            top_card_index = len(pile.face_up_cards) - 1
            if card_index >= top_card_index - 4:
                self.dragging = True
                self.drag_card = (pile_index, card_index)
                card_rect = self.get_card_rect(pile_index, card_index)
                self.drag_start_pos = pos
                self.drag_offset = (pos[0] - card_rect.x, pos[1] - card_rect.y)
                return

    def handle_mouse_up(self, pos: Tuple[int, int]):
        """处理鼠标释放事件"""
        if self.dragging and self.drag_card:
            # 检查是否可以放置到结算区域
            if self.settlement_area_rect.collidepoint(pos):
                from_pile, from_index = self.drag_card
                pile = self.game.piles[from_pile]
                cards_to_settle = pile.face_up_cards[from_index:]
                # 只在没有展示中的卡牌时才允许新展示
                if not self.settlement_display_cards:
                    self.settlement_display_cards = list(cards_to_settle)
                    self.settlement_display_timer = time.time()
                    self.settlement_display_from_pile = (from_pile, from_index)
                # 不立即移除和结算
            else:
                # 检查是否可以放置到其他牌堆
                for pile_index, pile in enumerate(self.game.piles):
                    pile_rect = pygame.Rect(
                        pile_start_x + pile_index * (self.card_width + card_spacing),
                        self.pile_area_y,  # 更新牌堆位置
                        self.card_width,
                        self.card_height * 3
                    )
                    if pile_rect.collidepoint(pos):
                        from_pile, from_index = self.drag_card
                        if from_pile != pile_index:
                            # 难度为1时限制移动次数
                            if self.difficulty == 1:
                                # 判断是否新回合（可根据你实际的回合切换逻辑调整）
                                now_turn = self.game.player.hp + sum(len(pile.cards) for pile in self.game.piles)
                                if self.last_turn != now_turn:
                                    self.move_count = 0
                                    self.last_turn = now_turn
                                self.move_count += 1
                                if self.move_count > self.move_limit:
                                    self.game.player.take_damage(1)
                            success, message = self.game.move_cards(from_pile, pile_index, from_index)
            # 重置拖动状态
            self.dragging = False
            self.drag_card = None
            self.drag_offset = (0, 0)

    def handle_events(self, events):
        """处理所有游戏事件"""
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if self.assets.modal_popup:
                        self.assets.modal_popup.toggle()
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
                    result = self.select_card_at_pos(mouse_pos)
                    if result is not None:
                        pile_index, card_index = result
                        pile = self.game.piles[pile_index]
                        top_index = len(pile.face_up_cards) - 1
                        if card_index >= top_index - 4:
                            self.dragging = True
                            self.drag_card = (pile_index, card_index)
                            card_rect = self.get_card_rect(pile_index, card_index)
                            self.drag_offset = (mouse_pos[0] - card_rect.x, mouse_pos[1] - card_rect.y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging:
                    # 检查是否可以放置到结算区域
                    if self.settlement_area_rect.collidepoint(event.pos):
                        from_pile, from_index = self.drag_card
                        pile = self.game.piles[from_pile]
                        cards_to_settle = pile.face_up_cards[from_index:]
                        # 只在没有展示中的卡牌时才允许新展示
                        if not self.settlement_display_cards:
                            self.settlement_display_cards = list(cards_to_settle)
                            self.settlement_display_timer = time.time()
                            self.settlement_display_from_pile = (from_pile, from_index)
                        # 不立即移除和结算
                    else:
                        # 检查是否可以放置到其他牌堆
                        for pile_index, pile in enumerate(self.game.piles):
                            pile_rect = pygame.Rect(
                                pile_start_x + pile_index * (self.card_width + card_spacing),
                                self.pile_area_y,  # 更新牌堆位置
                                self.card_width,
                                self.card_height * 3
                            )
                            if pile_rect.collidepoint(event.pos):
                                from_pile, from_index = self.drag_card
                                if from_pile != pile_index:
                                    # 难度为1时限制移动次数
                                    if self.difficulty == 1:
                                        # 判断是否新回合（可根据你实际的回合切换逻辑调整）
                                        now_turn = self.game.player.hp + sum(len(pile.cards) for pile in self.game.piles)
                                        if self.last_turn != now_turn:
                                            self.move_count = 0
                                            self.last_turn = now_turn
                                        self.move_count += 1
                                        if self.move_count > self.move_limit:
                                            self.game.player.take_damage(1)
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
                    # 检查卡牌悬停
                    self.hovered_card = self.select_card_at_pos(mouse_pos)
        return True

    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            # 处理事件
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    break

            # 如果弹窗显示，暂停所有游戏功能
            if self.assets.modal_popup and self.assets.modal_popup.is_active:
                # 只处理弹窗相关的事件
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        self.assets.modal_popup.toggle()
                self.assets.modal_popup.draw()
                pygame.display.flip()
                self.clock.tick(60)
                continue

            # 处理事件和更新游戏状态
            running = self.handle_events(events)
            self.draw()
            self.clock.tick(60)
            
            # 处理modal_popup
            if self.assets.modal_popup:
                self.assets.modal_popup.draw()
            
            pygame.display.flip()

            # 检查游戏状态
            if self.game.check_game_over():
                print("游戏结束！")
                running = False
            elif self.game.check_win_condition():
                print("恭喜获胜！")
                running = False

        pygame.quit()
        sys.exit()
