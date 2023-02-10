import pygame
from tools import SPACESHIP_IMAGE, SPACESHIP_IMAGE_HEIGHT

class Spaceship():

    def __init__(self, position_y) -> None:

        self.image_path = SPACESHIP_IMAGE
        self.position_y = position_y
        self.position_x = 40
        self.speed = 8
        self.lives = 3
    
    def draw(self, surface):
        spaceship = pygame.image.load(self.image_path)
        surface.blit(spaceship, (self.position_x, self.position_y))
    
    def move(self, surface):
        if pygame.key.get_pressed()[pygame.K_UP] and self.position_y > 0:
            self.position_y -= self.speed
        if pygame.key.get_pressed()[pygame.K_DOWN] and self.position_y < (surface.get_height() - SPACESHIP_IMAGE_HEIGHT):
            self.position_y += self.speed

