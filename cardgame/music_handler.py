from re import T
import pygame
from typing import Optional

class MusicHandler:
    def __init__(self):
        pygame.mixer.init()
        self.current_music: Optional[str] = None
        self.is_playing = True

    def play_music(self, music_file: str, loop: bool = True):
        """播放音乐
        Args:
            music_file: 音乐文件路径
            loop: 是否循环播放
        """
        if self.is_playing:
            pygame.mixer.music.stop()
        
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1 if loop else 0)
        self.current_music = music_file
        self.is_playing = True

    def stop_music(self):
        """停止音乐"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_music = None

    def pause_music(self):
        """暂停音乐"""
        if self.is_playing:
            pygame.mixer.music.pause()

    def resume_music(self):
        """恢复音乐"""
        if not self.is_playing and self.current_music:
            pygame.mixer.music.unpause()
            self.is_playing = True

# 创建单例实例
music_handler = MusicHandler()
