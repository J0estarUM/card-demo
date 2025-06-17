import pygame
from typing import Optional, Dict

class MusicHandler:
    def __init__(self):
        pygame.mixer.init()
        self.current_music: Optional[str] = None
        self.is_playing = True
        # 音效预加载字典
        self.sound_cache: Dict[str, pygame.mixer.Sound] = {}
        # 音效频道池
        self.channels = [pygame.mixer.Channel(i) for i in range(8)]  # 默认8个频道

    def play_music(self, music_file: str, loop: bool = True):
        """播放背景音乐
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
        """停止背景音乐"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_music = None

    def pause_music(self):
        """暂停背景音乐"""
        if self.is_playing:
            pygame.mixer.music.pause()

    def resume_music(self):
        """恢复背景音乐"""
        if not self.is_playing and self.current_music:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def load_sound(self, sound_file: str) -> pygame.mixer.Sound:
        """加载音效到缓存
        Args:
            sound_file: 音效文件路径
        Returns:
            pygame.mixer.Sound对象
        """
        if sound_file not in self.sound_cache:
            self.sound_cache[sound_file] = pygame.mixer.Sound(sound_file)
        return self.sound_cache[sound_file]

    def play_sound(self, sound_file: str, loop: bool = False, volume: float = 1.0):
        """播放音效
        Args:
            sound_file: 音效文件路径
            loop: 是否循环播放
            volume: 音量(0.0-1.0)
        """
        sound = self.load_sound(sound_file)
        # 获取空闲的频道
        for channel in self.channels:
            if not channel.get_busy():
                channel.set_volume(volume)
                channel.play(sound, -1 if loop else 0)
                return True
        return False

    def stop_sound(self, sound_file: str):
        """停止指定音效
        Args:
            sound_file: 音效文件路径
        """
        sound = self.load_sound(sound_file)
        for channel in self.channels:
            if channel.get_busy() and channel.get_sound() == sound:
                channel.stop()

# 创建单例实例
music_handler = MusicHandler()
