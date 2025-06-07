from game import Game
from gui import GameGUI, StartMenu
from config import screen_width, screen_height
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    # 先显示开始界面
    StartMenu(screen).run()
    # 创建游戏实例
    game = Game()
    # 创建GUI并运行
    gui = GameGUI(game)
    gui.run()

if __name__ == "__main__":
    main() 