import pygame
from beginning import Beginning
from tools import SCREEN_HEIGHT, SCREEN_WIDTH
from spaceship import Spaceship
from game import Game

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

stay = True

while stay:
    
    begin = Beginning(screen)
    new_game = begin.screen_loop()

    if new_game:
        spaceship = Spaceship()
        game = Game(screen, spaceship)
        game.start()