from this import d
import pygame
from config import screen_width, screen_height
from game import Game
from gui import GameGUI
from start_menu import StartMenu
from rule.rule_menu import RuleMenu
from music_handler import music_handler
from rule.difficulty import DifficultyMenu
from rule.modal_popup import ModalPopup
from rule.end_menu import EndMenu
from rule.loading import LoadingScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # 创建弹窗实例
    modal_popup = ModalPopup(screen)
    while True:
        # 先显示开始界面
        menu_result = StartMenu(screen).run()
        if menu_result == "exit":
            break
        # 创建游戏实例
        game = Game()
        def start_game(difficulty):
            gui = GameGUI(game, difficulty=difficulty, modal_popup=modal_popup)
            gui.run()
            # 检查是否胜利
            if game.check_win_condition():
                EndMenu(screen, game, is_win=True).run()
                # 胜利后显示加载界面
                loading_screen = LoadingScreen(screen, lambda: start_game(difficulty))
                loading_screen.run()
            else:
                EndMenu(screen, game, is_win=False).run()
        rule_menu = RuleMenu(screen, start_game)
        rule_menu.modal_popup = modal_popup
        rule_menu.run()

if __name__ == "__main__": 
    main()