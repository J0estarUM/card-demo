import pygame
from pygame.locals import *
import numpy as np

class ModalPopup:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.is_active = False
        self.background_blur = None
        
        # 计算弹窗大小（屏幕的80%）
        self.popup_width = int(screen.get_width() * 0.8)
        self.popup_height = int(screen.get_height() * 0.8)
        self.popup_rect = pygame.Rect(
            (screen.get_width() - self.popup_width) // 2,
            (screen.get_height() - self.popup_height) // 2,
            self.popup_width,
            self.popup_height
        )

    def apply_blur(self, surface, amount=10):
        """应用高斯模糊效果"""
        array = pygame.surfarray.array3d(surface)
        blurred = np.zeros_like(array)
        
        # 应用高斯模糊
        for i in range(3):
            blurred[:,:,i] = np.convolve(array[:,:,i].flatten(), 
                                       np.ones(amount)/amount, 
                                       mode='same').reshape(array[:,:,i].shape)
        
        return pygame.surfarray.make_surface(blurred)

    def handle_event(self, event):
        """处理事件"""
        if event.type == KEYDOWN and event.key == K_TAB:
            self.is_active = not self.is_active

    def draw(self):
        """绘制弹窗"""
        if not self.is_active:
            return
            
        # 绘制模糊背景
        if self.background_blur:
            self.screen.blit(self.background_blur, (0, 0))
        
        # 创建弹窗表面
        popup_surface = pygame.Surface((self.popup_width, self.popup_height), pygame.SRCALPHA)
        popup_surface.fill((255, 255, 255, 100))  # 半透明白色
        
        # 绘制边框
        border_rect = pygame.Rect(0, 0, self.popup_width, self.popup_height)
        pygame.draw.rect(popup_surface, (0, 0, 0), border_rect, 3)
        
        # 绘制内容
        font = pygame.font.Font(None, 36)
        text = font.render("弹窗内容", True, (0, 0, 0))
        text_rect = text.get_rect(center=border_rect.center)
        popup_surface.blit(text, text_rect)
        
        # 绘制弹窗到屏幕上
        self.screen.blit(popup_surface, self.popup_rect)

    def toggle(self):
        """切换弹窗显示状态"""
        self.is_active = not self.is_active
        if self.is_active:
            # 如果显示弹窗，获取当前屏幕并模糊
            self.background_blur = self.apply_blur(self.screen.copy())
        else:
            # 如果隐藏弹窗，清空模糊背景
            self.background_blur = None
        return True  # 返回True表示需要刷新界面
