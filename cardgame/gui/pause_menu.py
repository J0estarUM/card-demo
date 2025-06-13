import pygame
from pygame.locals import *
from typing import Callable
import time
from config import screen_width, screen_height, SCALE

class PauseMenu:
    def __init__(self, screen: pygame.Surface, resume_game: Callable[[], None], exit_game: Callable[[], None]):
        """
        初始化暂停菜单
        
        Args:
            screen: pygame.Surface 对象
            resume_game: 恢复游戏的回调函数
            exit_game: 退出游戏的回调函数
        """
        self.screen = screen
        self.resume_game = resume_game
        self.exit_game = exit_game
        self.running = True
        
        # 菜单选项
        self.options = [
            "继续游戏",
            "退出游戏"
        ]
        
        # 当前选中项
        self.selected_option = 0
        
        # 菜单位置和大小
        self.menu_width = int(400 * SCALE)
        self.menu_height = int(200 * SCALE)
        self.menu_x = (screen_width - self.menu_width) // 2
        self.menu_y = (screen_height - self.menu_height) // 2
        
        # 文字配置
        self.font = pygame.font.Font("assets/font/IPix.ttf", int(48 * SCALE))
        self.option_font = pygame.font.Font("assets/font/IPix.ttf", int(36 * SCALE))
        
        # 颜色
        self.menu_color = (50, 50, 50, 180)  # 半透明黑色
        self.text_color = (255, 255, 255)
        self.selected_color = (0, 255, 255)  # 选中时使用蓝色
        
    def handle_events(self, events: list[pygame.event.Event]):
        """处理事件"""
        for event in events:
            if event.type == QUIT:
                self.running = False
                self.exit_game()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # 再按 ESC 返回游戏
                    self.running = False
                elif event.key == K_UP:
                    self.selected_option = max(0, self.selected_option - 1)
                elif event.key == K_DOWN:
                    self.selected_option = min(len(self.options) - 1, self.selected_option + 1)
                elif event.key == K_RETURN:  # 按回车键确认选择
                    if self.selected_option == 0:
                        self.running = False
                    else:
                        self.running = False
                        self.exit_game()

    def draw(self):
        """绘制暂停菜单"""
        # 创建半透明背景
        menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)
        pygame.draw.rect(menu_surface, self.menu_color, (0, 0, self.menu_width, self.menu_height), border_radius=int(15 * SCALE))
        
        # 绘制标题
        title_text = self.font.render("游戏暂停", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.menu_width // 2, int(50 * SCALE)))
        menu_surface.blit(title_text, title_rect)
        
        # 绘制选项
        y_offset = int(120 * SCALE)
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.text_color
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.menu_width // 2, y_offset))
            menu_surface.blit(option_text, option_rect)
            y_offset += int(60 * SCALE)
        
        # 将菜单绘制到屏幕上
        self.screen.blit(menu_surface, (self.menu_x, self.menu_y))

    def run(self):
        """运行暂停菜单"""
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)
            
            # 绘制游戏界面
            self.screen.fill((0, 0, 0))  # 这里需要根据实际情况修改
            
            # 绘制暂停菜单
            self.draw()
            
            pygame.display.flip()
            clock.tick(60)
