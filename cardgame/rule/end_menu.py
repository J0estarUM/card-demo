import pygame
from pygame.locals import *
from typing import Callable
import time
from music_handler import music_handler
from config import screen_width, screen_height, SCALE

class EndMenu:
    # 文字配置
    TEXT_X_OFFSET = 100 * SCALE
    TEXT_Y_OFFSET = 200 * SCALE
    TEXT_LINE_HEIGHT = 40 * SCALE
    TEXT_COLOR = (255, 255, 255)
    TEXT_FONT_SIZE = int(36 * SCALE)
    
    # 结束界面文本
    END_TEXTS = {
        "win": [
            "恭喜你完成了仪式！",
            f"你成功收集了 {52} 点诅咒之力",
            "点击任意键返回主菜单"
        ],
        "lose": [
            "游戏结束",
            "你未能完成仪式",
            "点击任意键返回主菜单"
        ]
    }

    def __init__(self, screen: pygame.Surface, game, is_win: bool = False):
        self.screen = screen
        self.game = game
        self.is_win = is_win
        self.running = True
        self.current_text_index = 0
        self.bg_img = None
        self.font = None
        self.load_assets()

    def load_assets(self):
        try:
            self.bg_img = pygame.image.load("assets/backgrounds/end_background.png").convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (screen_width, screen_height))
        except Exception as e:
            self.bg_img = pygame.Surface((screen_width, screen_height))
            self.bg_img.fill((30, 60, 120))
            print(f"Failed to load background image: {e}")
        
        try:
            self.font = pygame.font.Font("assets/font/IPix.ttf", 24)
        except Exception as e:
            print(f"Failed to load font: {e}")
            self.font = pygame.font.SysFont('SimHei', 24)
    
    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                self.running = False

    def draw(self):
        # 绘制背景
        self.screen.blit(self.bg_img, (0, 0))
        
        # 获取当前应该显示的文本
        texts = self.END_TEXTS["win"] if self.is_win else self.END_TEXTS["lose"]
        
        # 绘制文本
        y = self.TEXT_Y_OFFSET
        for text in texts:
            text_surface = self.font.render(text, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += self.TEXT_LINE_HEIGHT

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)
            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def cleanup(self):
        music_handler.stop_music()