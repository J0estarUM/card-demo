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

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # 创建弹窗实例
    modal_popup = ModalPopup(screen)
    # 先显示开始界面
    StartMenu(screen).run()
    # 创建游戏实例
    game = Game()
    def start_game(difficulty):
        gui = GameGUI(game, difficulty=difficulty, modal_popup=modal_popup)
        gui.run()
    rule_menu = RuleMenu(screen, start_game)
    rule_menu.modal_popup = modal_popup
    rule_menu.run()
    # 游戏结束后显示结算界面
    EndMenu(screen, gui.game).run()

if __name__ == "__main__": 
    main()