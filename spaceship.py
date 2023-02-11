import pygame
from tools import SPACESHIP_IMAGE, SPACESHIP_IMAGE_HEIGHT, SPACESHIP_IMAGE_WIDTH

class Spaceship():

    def __init__(self, position_y):

        self.image_path = SPACESHIP_IMAGE
        self.position_y = position_y
        self.position_x = 0
        self.speed = 14
        self.lives = 3
        self.score = 0
    
    def draw(self, surface):
        spaceship = pygame.image.load(self.image_path)
        surface.blit(spaceship, (self.position_x, self.position_y))
    
    def move(self, surface):
        if pygame.key.get_pressed()[pygame.K_UP] and self.position_y > 0:
            self.position_y -= self.speed
        if pygame.key.get_pressed()[pygame.K_DOWN] and self.position_y < (surface.get_height() - SPACESHIP_IMAGE_HEIGHT):
            self.position_y += self.speed
    
    def score_crash_verification(self, obstacles):
        crash = False
        game_over = False
        new_obstacle = obstacles
        for index, obstacle in enumerate(obstacles):
            if obstacle.position_x + obstacle.image_width <= 0:
                self.score += 1
                new_obstacle.pop(index)
            if ( self.position_x + SPACESHIP_IMAGE_WIDTH >= obstacle.position_x and
                obstacle.position_x + obstacle.image_width >= self.position_x and
                self.position_y + SPACESHIP_IMAGE_HEIGHT >= obstacle.position_y and
                obstacle.position_y + obstacle.image_width >= self.position_y ):
                crash = True
                new_obstacle.pop(index)
                self.lives -= 1
                if self.lives < 1:
                    game_over = True
        return [crash, game_over, new_obstacle]