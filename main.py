import sys

import pygame

from src.game import Game

if __name__ == "__main__":
    # Function main
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
