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
    END_TEXTS = [
        "游戏结束",
        "感谢您的游玩！",
        "点击任意键返回主菜单"
    ]

    def __init__(self, screen: pygame.Surface, game):
        self.screen = screen
        self.game = game
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

    def update(self):
        self.screen.blit(self.bg_img, (0, 0))
        font = pygame.font.Font("assets/font/IPix.ttf", int(self.TEXT_FONT_SIZE))
        
        lines = [line for line in self.END_TEXTS[self.current_text_index].split('\n') if line.strip()]
        total_height = len(lines) * self.TEXT_LINE_HEIGHT
        start_y = (screen_height - total_height) // 2

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect()
            text_rect.centerx = screen_width // 2
            text_rect.y = start_y + i * self.TEXT_LINE_HEIGHT
            self.screen.blit(text_surface, text_rect)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            self.handle_events(events)
            self.update()
            pygame.display.flip()
            clock.tick(60)
        
        return False

    def cleanup(self):
        music_handler.stop_music()