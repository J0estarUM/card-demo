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
        self.rule_texts = [
            "黑塔内部规则小告示",
            "卡牌种类\n进攻卡,防御卡,生命卡,诅咒卡$攻击和血量都是卡牌上的数值$",
            "卡堆规则\n6堆牌,自由降序堆叠,拖入$中下部$的验证区进行验证",
            "验证规则\n一次验证小于等于5张牌,$防御$大于等于$诅咒值$等于不扣血,$攻击$大于$诅咒值$等于击败；\n否则扣血并且卡回流",
            "生命系统\n初始生命10点,可用生命卡恢复",
            "胜利\n消除的诅咒牌累加达到52即胜利,生命为0即失败"
        ]


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
        
        # 设置字体
        title_font = pygame.font.Font("assets/font/IPix.ttf", 48)
        normal_font = pygame.font.Font("assets/font/IPix.ttf", 24)

        # 计算所有文本的总高度
        total_height = len(self.rule_texts) * (normal_font.get_height() + 10) # 每行文本高度+行间距
        start_y = border_rect.centery - total_height // 2 - 200  # 从弹窗垂直中心开始
        line_height = normal_font.get_height() + 50 # 每行文本高度+行间距
        text_x = border_rect.left + 150  # 从左边留出30像素的边距

       
        # 渲染第一行文本（使用不同颜色）
        first_text = self.rule_texts[0]
        rendered_first = title_font.render(first_text, True, (0, 0, 0))  # 使用紫色
        first_rect = rendered_first.get_rect()
        first_rect.topleft = (text_x, start_y)
        popup_surface.blit(rendered_first, first_rect)
        start_y += line_height

        # 渲染剩余文本，处理换行
        for text in self.rule_texts[1:]:
            # 分割文本
            lines = text.split('\n')
            for line in lines:
                rendered_text = normal_font.render(line, True, (0, 0, 0))
                text_rect = rendered_text.get_rect()
                text_rect.topleft = (text_x, start_y)
                popup_surface.blit(rendered_text, text_rect)
                start_y += normal_font.get_height() + 10  # 每行之间留出10像素间距
            # 在每个规则之间留出更大的间距
            start_y += 40
        
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
