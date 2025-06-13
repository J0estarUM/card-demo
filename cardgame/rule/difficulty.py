import pygame
from pygame.locals import *
from typing import Callable
import time
from music_handler import music_handler
from config import screen_width, screen_height, SCALE
from .loading import LoadingScreen

class DifficultyMenu:
    def __init__(self, screen: pygame.Surface, return_to_game: Callable[[], None] = None):
        self.screen = screen
        self.return_to_game = return_to_game
        self.running = True
        self.selected_difficulty = None
        
        # 设置难度框的参数（调整为更大的尺寸）
        self.box_width = int(600 * SCALE)  
        self.box_height = int(500 * SCALE)  
        self.box_margin = int(50 * SCALE)
        
        # 计算两个难度框的位置（调整位置以适应更大的框）
        self.box_positions = [
            (screen_width // 4 - self.box_width // 2, 
             screen_height // 2 - self.box_height // 2 ),  # 向上移动50像素
            (3 * screen_width // 4 - self.box_width // 2, 
             screen_height // 2 - self.box_height // 2 )   # 向上移动50像素
        ]
        # 文字配置
        self.TEXT_X_OFFSET = 100 * SCALE  # 根据缩放比例调整
        self.TEXT_Y_OFFSET = 80 * SCALE  # 调整为80，使文字更靠近顶部
        self.TEXT_LINE_HEIGHT = 50 * SCALE  # 行间距增加到60
        # 文字颜色配置
        self.TITLE_COLOR = (0, 255, 255)  # 标题使用蓝色
        self.DESC1_COLOR = (255, 255, 255)  # 第2-4行使用白色
        self.DESC2_COLOR = (0, 255, 180)  # 剩余行使用绿色
        self.TITLE_FONT_SIZE = int(48 * SCALE)  # 标题字体大小
        self.DESC_FONT1_SIZE = int(24 * SCALE)  # 描述文字字体大小
        self.DESC_FONT2_SIZE = int(18 * SCALE)  # 描述文字行间距

        # 难度描述
        self.difficulty_texts = [
            "$无束之径$\n黑塔不会干涉你的行动,也不设置任何限制\n你可以自由地移动卡牌,布置牌堆,调整策略\n这条道路只考验你的智慧与耐心\n没有移动限制\n任何时候都可以自由组合与操作牌堆\n适合新手玩家或希望专注解谜 策略布局的体验者\n游戏节奏偏平缓,但对整体局势把控要求较高",
            "$血之誓约$\n每一步都是权衡,每一次移动都是抉择\n在这条道路上,你只能做出有限次数的操作\n但若你愿意 也可以用自己的血撕裂命运的限制\n每轮移动次数有限,每轮可移动3次\n若超出次数,额外操作将扣除生命值\n战术感更强,对资源管理与节奏控制要求更高\n适合高阶玩家,挑战感更强烈"
        ]
        
        # 颜色设置（RGB值）
        self.normal_color = (128, 128, 128)
        self.hover_color = (150, 150, 150)
        self.selected_color = (200, 200, 200)
        
        # 透明度设置（0-255，值越大越不透明）
        self.normal_alpha = 128  # 半透明
        self.hover_alpha = 180   # 稍微更不透明
        self.selected_alpha = 200 # 更不透明
        
        # 初始化状态
        self.hovered_box = None
        self.selected_box = None
        
        self.font = pygame.font.Font(None, int(36 * SCALE))
        self.load_assets()

    def load_assets(self):
        # 加载背景
        try:
            self.bg_img = pygame.image.load("assets/backgrounds/background.png").convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (screen_width, screen_height))
        except Exception as e:
            self.bg_img = pygame.Surface((screen_width, screen_height))
            self.bg_img.fill((30, 60, 120))
            print(f"Failed to load background image: {e}")
        
        # 设置字体
        try:
            self.title_font = pygame.font.Font("assets/font/IPix.ttf", self.TITLE_FONT_SIZE)
            self.desc_font1 = pygame.font.Font("assets/font/IPix.ttf", self.DESC_FONT1_SIZE)
            self.desc_font2 = pygame.font.Font("assets/font/IPix.ttf", self.DESC_FONT2_SIZE)
        except Exception as e:
            print(f"Failed to load font: {e}")
            self.title_font = pygame.font.SysFont('SimHei', self.TITLE_FONT_SIZE)
            self.desc_font1 = pygame.font.SysFont('SimHei', self.DESC_FONT1_SIZE)
            self.desc_font2 = pygame.font.SysFont('SimHei', self.DESC_FONT2_SIZE)

    def draw_box(self, index, position, color):
        """绘制难度框"""
        # 创建一个与框大小相同的Surface
        box_surface = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)
        
        # 根据状态设置不同的透明度
        if self.selected_box == index:
            alpha = self.selected_alpha
        elif self.hovered_box == index:
            alpha = self.hover_alpha
        else:
            alpha = self.normal_alpha
        
        # 在Surface上绘制矩形
        pygame.draw.rect(box_surface, (*color, alpha), 
                         (0, 0, self.box_width, self.box_height), 
                         border_radius=int(15 * SCALE))
        
        # 将Surface绘制到屏幕上
        self.screen.blit(box_surface, position)
        
        # 绘制难度描述文字
        lines = self.difficulty_texts[index].split("\n")
        y_offset = position[1] + self.TEXT_Y_OFFSET
        
        # 第一行作为标题，使用大号字体和黄色
        title_text = lines[0]
        title_surface = self.title_font.render(title_text, True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(
            position[0] + self.box_width // 2, 
            y_offset
        ))
        self.screen.blit(title_surface, title_rect)
        y_offset += self.TEXT_LINE_HEIGHT
        
        # 第2、3、4行使用字体1和白色
        for i, line in enumerate(lines[1:4], 1):
            desc1_surface = self.desc_font1.render(line, True, self.DESC1_COLOR)
            desc1_rect = desc1_surface.get_rect(center=(
                position[0] + self.box_width // 2, 
                y_offset
            ))
            self.screen.blit(desc1_surface, desc1_rect)
            y_offset += self.TEXT_LINE_HEIGHT
        
        # 剩余行使用字体2和灰色
        for line in lines[4:]:
            desc2_surface = self.desc_font2.render(line, True, self.DESC2_COLOR)
            desc2_rect = desc2_surface.get_rect(center=(
                position[0] + self.box_width // 2, 
                y_offset
            ))
            self.screen.blit(desc2_surface, desc2_rect)
            y_offset += self.TEXT_LINE_HEIGHT

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                return False
                
            if event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                self.hovered_box = None
                for i, pos in enumerate(self.box_positions):
                    box_rect = pygame.Rect(pos[0], pos[1], 
                                         self.box_width, self.box_height)
                    if box_rect.collidepoint(mouse_pos):
                        self.hovered_box = i
                        break
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, pos in enumerate(self.box_positions):
                    box_rect = pygame.Rect(pos[0], pos[1], 
                                         self.box_width, self.box_height)
                    if box_rect.collidepoint(mouse_pos):
                        self.selected_box = i
                        self.running = False  # 选择难度后退出菜单
                        return True
        return False

    def run(self):
        clock = pygame.time.Clock()
        self.load_assets()
        while self.running:
            if self.handle_events():
                break
            
            self.screen.blit(self.bg_img, (0, 0))
            
            # 绘制两个难度框
            for i, pos in enumerate(self.box_positions):
                color = self.normal_color
                if self.hovered_box == i:
                    color = self.hover_color
                if self.selected_box == i:
                    color = self.selected_color
                self.draw_box(i, pos, color)
            
            pygame.display.flip()
            clock.tick(60)

        # 返回选择的难度（0: 简单, 1: 困难）
        # 返回参数在这里！！！！！！
        return self.selected_box if self.selected_box is not None else 0