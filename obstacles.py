import random

import pygame
from tools import OBSTACLES_TYPES_IMAGES, SCREEN_HEIGHT, SCREEN_WIDTH


class Obstacles():

    def __init__(self, speed):
        obstacles_types = list(OBSTACLES_TYPES_IMAGES)
        self.type = obstacles_types[random.randint(0, len(obstacles_types)-1)]
        self.image_path = OBSTACLES_TYPES_IMAGES[self.type]
        self.image_width = random.randint(50, 100)
        self.speed = speed
        self.position_x = SCREEN_WIDTH
        self.position_y = random.random() * (SCREEN_HEIGHT - self.image_width)

    def draw(self, surface):
        obstacle = pygame.image.load(self.image_path)
        obstacle_resizing = pygame.transform.scale(obstacle, (self.image_width, self.image_width))
        surface.blit(obstacle_resizing, (self.position_x, self.position_y))
    
    def move(self):
         self.position_x -= self.speed