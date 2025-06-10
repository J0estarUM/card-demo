import pygame
from pygame.locals import *
from typing import Callable
import time
from music_handler import music_handler
from config import screen_width, screen_height, START_BTN_SIZE, SCALE

# 定义规则菜单类
class RuleMenu:
    LOADING_DURATION = 4  # 加载动画持续时间（秒）

    # 加载动画配置
    LOADING_IMG = "assets/backgrounds/loading1.png"
    LOADING_IMG_SIZE = (1200 , 600)  # 根据缩放比例调整尺寸

    # 文字配置
    TEXT_X_OFFSET = 100 * SCALE  # 根据缩放比例调整
    TEXT_Y_OFFSET = 200 * SCALE  # 根据缩放比例调整
    TEXT_LINE_HEIGHT = 40 * SCALE  # 根据缩放比例调整
    TEXT_COLOR = (255, 255, 255)
    TEXT_FONT_SIZE = int(36 * SCALE)  # 根据缩放比例调整

    # 规则文本版本
    RULE_TEXTS = [
        """
            ░ 远古的罪 ░
        第五纪元末日降临，天空燃烧，大地崩解，众神弃世。
        那一夜，黑塔从地心升起，携带着七十二封印中最深的一道——【诅咒之契】。
        
        众生哀嚎、魂灵消散，唯有一人——你，被"塔楼记录者"选中，成为夜行者。
        
        你不是来拯救世界的。你是来完成仪式的。
        """,
        """
           ░ 诅咒之力 ░
传说中，每一张卡牌，都是陨落灵魂的哀号残片。
当你抽出这些牌，你不仅是在作战，更是在唤醒诅咒本源。

进攻牌：以血还血，以刃驱散恐惧。

防御牌：承载意志的壁垒，抵御灵魂的侵蚀。

生命牌：从腐朽中汲取残存的温度。

诅咒牌：最为危险，亦最为关键。它们是敌人，也是你通往终点的“祭品”。

每一次面对诅咒，你都必须做出选择：驱散它，或接受它。
每当你击败一张诅咒卡，你可选择将它吞噬——将其转化为诅咒值。

只有当你吞噬足够多的诅咒之力——达到52点诅咒值，你才能进入黑塔之巅，完成仪式，结束这一切。
**代价是什么？**没人知道。也许是灵魂的永坠，也许是整个世界的重构。
        """,
        """
░ 仪式的代价 ░
52夜，52次考验，52次决断。

你会获得遗物，它们会给予你力量，也会慢慢侵蚀你的心智。
你会获得卡牌，它们会组成你的武装，也可能成为你败亡的根源。
你会遇见影子般的灵体，那是曾失败的夜行者残魂，他们会低语，会试图阻止你继续前进。

因为——
这个世界，并不希望你成功。
成功的代价，是打破封印；而封印的背后，埋藏的是最初的真相。
""",
"""
░ 结语 ░
你要达成的，不是救赎。是完成这场无法中断的仪式。
用52点诅咒值，打开那扇封印的大门——
黑塔之巅，等你到来。
"""
    ]

    def __init__(self, screen: pygame.Surface, return_to_game: Callable[[], None] = None):
        self.screen = screen
        self.return_to_game = return_to_game  # 返回游戏的回调函数
        self.running = True
        self.current_text_index = 0  # 初始化文本索引
       
        self.loading = False 
        self.bg_img = None
        self.loading_img = None
        self.eye_img = None
        self.juhao_img = None
        self.font = None
        
        self.load_assets()  # 加载资源

    def load_assets(self):
        # 加载背景
        try:
            self.bg_img = pygame.image.load("assets/backgrounds/background.png").convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (screen_width, screen_height))
        except Exception as e:
            self.bg_img = pygame.Surface((screen_width, screen_height))
            self.bg_img.fill((30, 60, 120))
            print(f"Failed to load background image: {e}")
        
        # 加载loading图片
        try:
            self.loading_img = pygame.image.load(self.LOADING_IMG).convert_alpha()
            self.loading_img = pygame.transform.smoothscale(self.loading_img, self.LOADING_IMG_SIZE)
            print(f"Loading image loaded successfully: {self.loading_img.get_size()}")
        except Exception as e:
            print(f"Failed to load loading image: {e}")
            self.loading_img = None
        
        
        # 设置字体
        try:
            self.font = pygame.font.Font("assets/font/IPix.ttf", 24)
        except Exception as e:
            print(f"Failed to load font: {e}")
            self.font = pygame.font.SysFont('SimHei', 24)
        
        # 规则文本
        self.rules_text = self.RULE_TEXTS[0]
    
    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if self.current_text_index < len(self.RULE_TEXTS) - 1:
                    self.current_text_index += 1
                    self.rules_text = self.RULE_TEXTS[self.current_text_index]
                else:
                    # 不直接播放加载动画，只是设置状态，留给主循环处理
                    self.loading = True
                    self.loading_start_time = time.time()

    def update(self):
        """更新界面"""
        self.screen.blit(self.bg_img, (0, 0))     
        # 设置字体
        font = pygame.font.Font("assets/font/IPix.ttf", int(self.TEXT_FONT_SIZE))
        
        # 绘制规则文本
        current_y = self.TEXT_Y_OFFSET
        for line in self.rules_text.split('\n'):
            if line.strip():  # 只绘制非空行
                text_surface = font.render(line, True, self.TEXT_COLOR)
                text_rect = text_surface.get_rect()
                text_rect.topleft = (self.TEXT_X_OFFSET, current_y)
                self.screen.blit(text_surface, text_rect)
                current_y += self.TEXT_LINE_HEIGHT
    
    def update_loading(self):
        # 先绘制背景
        self.screen.blit(self.bg_img, (0, 0))
        
        # 如果loading_img加载成功，绘制loading动画
        if self.loading_img:
            rect = self.loading_img.get_rect(center=(screen_width // 2, screen_height // 2))
            self.screen.blit(self.loading_img, rect)
        
        # 播放加载音乐
        if not hasattr(self, "_loading_music_played"):
            music_handler.play_music("assets/music/loading.mp3",False)
            self._loading_music_played = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            if self.loading:
                self.update_loading()
                if time.time() - self.loading_start_time > RuleMenu.LOADING_DURATION:
                    self.running = False
            else:
                self.handle_events(events)
                if self.loading:
                    if hasattr(self, "_loading_music_played"):
                        del self._loading_music_played
                self.update()  # 只在非loading状态下更新规则界面

            pygame.display.flip()
            

        if self.return_to_game:
            self.return_to_game()

    def cleanup(self):
        """清理资源"""
        music_handler.stop_music()
