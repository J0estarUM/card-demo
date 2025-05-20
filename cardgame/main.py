from game import Game
from gui import GameGUI

def main():
    # 创建游戏实例
    game = Game()
    
    # 创建GUI并运行
    gui = GameGUI(game)
    gui.run()

if __name__ == "__main__":
    main() 