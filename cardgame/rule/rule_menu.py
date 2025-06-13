import pygame
from pygame.locals import *
from typing import Callable
import time
from music_handler import music_handler
from config import screen_width, screen_height, SCALE
from rule.loading import LoadingScreen
from rule.difficulty import DifficultyMenu

# 定义规则菜单类
class RuleMenu:
    # 文字配置
    TEXT_X_OFFSET = 100 * SCALE  # 根据缩放比例调整
    TEXT_Y_OFFSET = 200 * SCALE  # 根据缩放比例调整
    TEXT_LINE_HEIGHT = 40 * SCALE  # 根据缩放比例调整
    TEXT_COLOR = (255, 255, 255)
    TEXT_FONT_SIZE = int(36 * SCALE)  # 根据缩放比例调整

    # 规则文本版本
    RULE_TEXTS = [
"""
世界已经崩坏了.
""",
"""
在过去的一场灾难中，诅咒如瘟疫般蔓延，吞噬了时间.生命和希望.
幸存者们说，这一切源于那座塔
诅咒之塔.
""",
"""
没人知道它从哪里来，但自从它出现后，世界开始被黑暗吞噬，
每过一个夜晚，就有更多的人被夺走.
""",
"""
现在,只剩下52个夜晚.
""",
"""
你是最后的执行者,被选中进入塔内完成多次危险的仪式
收集足够的诅咒之力,总值达到52点,唤醒沉睡在塔中的真相.
""",
"""
你要摸清靠卡牌作战,每一张牌都是你的工具.武器,或代价.
攻击牌...打击敌人,削弱诅咒.
防御牌...抵御伤害,保护自己.
生命牌...回复生命,延续存活.
诅咒牌...它们是敌人,但也是完成仪式的关键.
每一张诅咒牌可以对你同时展开攻击和防御的双重效果，
""",
"""
还有一些神秘的规则需要你自己摸索.
"""
"""
在每一场战斗中，你必须选择
是摧毁诅咒，还是接受它，成为你的一部分.
你越强大，诅咒也会越靠近你.
""",
"""
当时间逝去，末日降临，你将前往塔顶，面对最终的审判.
没有人知道，走到最后的人，会看到什么.
"""

    ]

    def __init__(self, screen: pygame.Surface, start_game: Callable[[], None] = None):
        self.screen = screen
        self.start_game = start_game  # 返回游戏的回调函数
        self.running = True
        self.current_text_index = 0  # 初始化文本索引
       
        self.loading = False 
        self.bg_img = None
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
                   self.show_difficulty()
    def update(self):
        """更新界面"""
        self.screen.blit(self.bg_img, (0, 0))     
        # 设置字体
        font = pygame.font.Font("assets/font/IPix.ttf", int(self.TEXT_FONT_SIZE))
        
        # 拆分文本行
        lines = [line for line in self.rules_text.split('\n') if line.strip()]
        # 计算总高度
        total_height = len(lines) * self.TEXT_LINE_HEIGHT
        # 计算起始y，使文本整体垂直居中
        start_y = (screen_height - total_height) // 2

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect()
        # 设置x为水平居中
            text_rect.centerx = screen_width // 2
        # 设置y为整体垂直居中
            text_rect.y = start_y + i * self.TEXT_LINE_HEIGHT
            self.screen.blit(text_surface, text_rect)

    def show_difficulty(self):
        """显示难度选择界面"""
        difficulty = DifficultyMenu(self.screen)
        difficulty.run()
        
        # 难度选择后显示加载动画
        loading_screen = LoadingScreen(self.screen, self.start_game)
        loading_screen.run()    
        
        # 结束规则界面
        self.running = False

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
            

    def cleanup(self):
        """清理资源"""
        music_handler.stop_music()
