import pygame
from pygame.locals import *
from typing import Callable
import time
from music_handler import music_handler
from config import screen_width, screen_height, SCALE

class LoadingScreen:
    LOADING_DURATION = 4  # 加载动画持续时间（秒）
    
    # 加载动画配置
    LOADING_IMG = "assets/backgrounds/loading1.png"
    LOADING_IMG_SIZE = (1200 * SCALE, 600 * SCALE)  # 根据缩放比例调整尺寸
    
    def __init__(self, screen: pygame.Surface, on_complete: Callable[[], None] = None):
        """
        初始化加载屏幕
        
        Args:
            screen: pygame.Surface 对象
            on_complete: 加载完成后的回调函数
        """
        self.screen = screen
        self.on_complete = on_complete
        self.running = True
        
        self.loading_img = None
        self.loading_start_time = None
        self._loading_music_played = False
        
        self.load_assets()
    
    def load_assets(self):
        """加载资源"""
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
    
    def update(self):
        """更新加载界面"""
        self.screen.blit(self.bg_img, (0, 0))
        
        # 如果loading_img加载成功，绘制loading动画
        if self.loading_img:
            rect = self.loading_img.get_rect(center=(screen_width // 2, screen_height // 2))
            self.screen.blit(self.loading_img, rect)
        
        # 播放加载音乐
        if not self._loading_music_played:
            music_handler.play_music("assets/music/loading.mp3", False)
            self._loading_music_played = True
    
    def run(self):
        """运行加载动画"""
        clock = pygame.time.Clock()
        self.loading_start_time = time.time()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
            
            self.update()
            pygame.display.flip()
            
            # 检查是否加载完成
            if time.time() - self.loading_start_time > self.LOADING_DURATION:
                self.running = False
        
        # 清理资源
        music_handler.stop_music()
        
        # 调用完成回调
        if self.on_complete:
            self.on_complete()