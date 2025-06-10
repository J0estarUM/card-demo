import pygame
import sys
from config import *
import time
from rule.rule_menu import RuleMenu
from music_handler import music_handler

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_img = None
        self.btn_img = None
        self.new_game_img = None
        self.btn_rect = None
        self.loadgame_btn_img = None
        self.loadgame_img = None
        self.loadgame_btn_rect = None
        self.title_img = None
        self.cloud1_img = None
        self.cloud2_img = None
        self.stars_img = None
        self.loading_img = None
        self.eye_img = None
        self.juhao_img = None
        self.cloud1_pos = list(CLOUD1_IMG_OFFSET)  # [x, y]
        self.cloud2_pos = None  # 右下角云朵的动态位置
        self.load_assets()
        # 初始化cloud2的起始位置
        if self.cloud2_img:
            cloud2_rect = self.cloud2_img.get_rect()
            self.cloud2_pos = [
                screen_width - CLOUD2_IMG_OFFSET[0] - cloud2_rect.width,
                screen_height - CLOUD2_IMG_OFFSET[1] - cloud2_rect.height
            ]

    def load_assets(self):
        # 加载背景
        try:
            self.bg_img = pygame.image.load(START_BG_IMG).convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (screen_width, screen_height))
        except Exception as e:
            self.bg_img = pygame.Surface((screen_width, screen_height))
            self.bg_img.fill((30, 60, 120))
        # 加载new game按钮图片
        try:
            self.btn_img = pygame.image.load(BTN_IMG).convert_alpha()
            self.btn_img = pygame.transform.smoothscale(self.btn_img, START_BTN_SIZE)
        except Exception as e:
            self.btn_img = pygame.Surface(START_BTN_SIZE, pygame.SRCALPHA)
            self.btn_img.fill((200, 180, 0, 220))
        self.btn_rect = self.btn_img.get_rect(center=(screen_width//2, screen_height//2))
        # 加载"new game"字样图片
        try:
            self.new_game_img = pygame.image.load(NEW_GAME_IMG).convert_alpha()
            self.new_game_img = pygame.transform.smoothscale(self.new_game_img, START_BTN_SIZE)
        except Exception as e:
            self.new_game_img = None
        # 加载load game按钮图片
        try:
            self.loadgame_btn_img = pygame.image.load(BTN_IMG).convert_alpha()
            self.loadgame_btn_img = pygame.transform.smoothscale(self.loadgame_btn_img, START_BTN_SIZE)
        except Exception as e:
            self.loadgame_btn_img = pygame.Surface(START_BTN_SIZE, pygame.SRCALPHA)
            self.loadgame_btn_img.fill((180, 180, 180, 220))
        self.loadgame_btn_rect = self.loadgame_btn_img.get_rect(center=(screen_width//2, screen_height//2+100))

        # 加载load game字样图片
        try:
            self.loadgame_img = pygame.image.load(LOADGAME_IMG).convert_alpha()
            self.loadgame_img = pygame.transform.smoothscale(self.loadgame_img, START_BTN_SIZE)
        except Exception as e:
            self.loadgame_img = None
        # 加载标题图片
        try:
            self.title_img = pygame.image.load(TITLE_IMG).convert_alpha()
            self.title_img = pygame.transform.smoothscale(self.title_img, TITLE_IMG_SIZE)
        except Exception as e:
            self.title_img = None
        # 加载cloud1图片
        try:
            self.cloud1_img = pygame.image.load(CLOUD1_IMG).convert_alpha()
            self.cloud1_img = pygame.transform.smoothscale(self.cloud1_img, CLOUD1_IMG_SIZE)
        except Exception as e:
            self.cloud1_img = None
        # 加载cloud2图片
        try:
            self.cloud2_img = pygame.image.load(CLOUD2_IMG).convert_alpha()
            self.cloud2_img = pygame.transform.smoothscale(self.cloud2_img, CLOUD2_IMG_SIZE)
        except Exception as e:
            self.cloud2_img = None
        # 加载stars图片
        try:
            self.stars_img = pygame.image.load(STARS_IMG).convert_alpha()
            self.stars_img = pygame.transform.smoothscale(self.stars_img, STARS_IMG_SIZE)
        except Exception as e:
            self.stars_img = None

    def run(self):
        music_handler.play_music("assets/music/home+rules.mp3", loop=True)
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_rect.collidepoint(event.pos):
                        running = False
                    elif self.loadgame_btn_rect.collidepoint(event.pos):
                        print("点击了Load Game按钮")
                    elif self.rule_btn_rect.collidepoint(event.pos):
                        rule_menu = RuleMenu(self.screen)
                        rule_menu.run()
                        rule_menu.cleanup()  # 清理资源

            # --- 云朵移动逻辑 ---
            # 云1向右移动
            self.cloud1_pos[0] += 0.2  # 速度可调
            if self.cloud1_pos[0] > screen_width:
                self.cloud1_pos[0] = -CLOUD1_IMG_SIZE[0]  # 循环回到左侧

            # 云2向右移动
            if self.cloud2_pos:
                self.cloud2_pos[0] += 0.1  # 速度可调
                if self.cloud2_pos[0] > screen_width:
                    self.cloud2_pos[0] = -CLOUD2_IMG_SIZE[0]

            # --- 绘制 ---
            self.screen.blit(self.bg_img, (0, 0))
            # 先绘制cloud1和cloud2图片
            if self.cloud1_img:
                self.screen.blit(self.cloud1_img, self.cloud1_pos)
            if self.cloud2_img and self.cloud2_pos:
                self.screen.blit(self.cloud2_img, self.cloud2_pos)
            # 再绘制stars图片
            if self.stars_img:
                offset_x, offset_y = STARS_IMG_OFFSET
                self.screen.blit(self.stars_img, (offset_x, offset_y))
            # 居中绘制标题图片
            if self.title_img:
                offset_x, offset_y = TITLE_IMG_OFFSET
                title_rect = self.title_img.get_rect(midtop=(screen_width//2 + offset_x, offset_y))
                self.screen.blit(self.title_img, title_rect)
            self.screen.blit(self.btn_img, self.btn_rect)
            if self.new_game_img:
                new_game_rect = self.new_game_img.get_rect(center=self.btn_rect.center)
                self.screen.blit(self.new_game_img, new_game_rect)
            self.screen.blit(self.loadgame_btn_img, self.loadgame_btn_rect)
            if self.loadgame_img:
                offset_x, offset_y = LOADGAME_TEXT_OFFSET
                loadgame_rect = self.loadgame_img.get_rect(center=(
                    self.loadgame_btn_rect.centerx + offset_x,
                    self.loadgame_btn_rect.centery + offset_y
                ))
                self.screen.blit(self.loadgame_img, loadgame_rect)

            pygame.display.flip()
            clock.tick(60)