import pygame
from screens import Beginning, Game, Game_Over
from objects import Spaceship
from tools import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

stay = True

while stay:
    
    begin = Beginning(screen)
    new_game = begin.screen_loop()

    if new_game:
        spaceship = Spaceship()
        game = Game(screen, spaceship)
        game.start()
        if game.game_over:
            end = Game_Over(screen)
            end.print_screen()
        