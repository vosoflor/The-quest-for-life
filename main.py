import pygame
from tools import SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE_HEIGHT
from spaceship import Spaceship
from game import Game

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
spaceship = Spaceship(screen.get_height()/2 - SPACESHIP_IMAGE_HEIGHT/2)
new_game = Game(screen, spaceship)
new_game.start_level()