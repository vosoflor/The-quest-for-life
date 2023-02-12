import pygame

from objects import Spaceship
from screens import Beginning, Game, Game_Over, Positions_Table
from tools import SCREEN_HEIGHT, SCREEN_WIDTH


class Scene_Controller():

    def __init__(self):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
    
    def play(self):

        stay = True

        while stay:
            
            begin = Beginning(self.screen)
            new_game = begin.screen_loop()

            if new_game:
                spaceship = Spaceship()
                game = Game(self.screen, spaceship)
                game.start()
                if game.game_over:
                    end = Game_Over(self.screen)
                    end.print_screen()
                    positions_table = Positions_Table(self.screen, game)
                    positions_table.check_score()
                    positions_table.print()