import pygame
from tools import PLANET_IMAGES_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE, SPACESHIP_IMAGE_HEIGHT, SPACESHIP_IMAGE_WIDTH

class Spaceship():

    def __init__(self, position_y):

        self.image_path = SPACESHIP_IMAGE
        self.position_y = position_y
        self.position_x = 0
        self.speed = 14
        self.lives = 3
        self.score = 0
        self.rotate = False
        self.rotation_angle = 0.4
        self.rotation_times = 1
    
    def draw(self, surface):
        spaceship = pygame.image.load(self.image_path)
        if self.rotate:
            if self.rotation_times < 450:
                rotated_spaceship = pygame.transform.rotate(spaceship, self.rotation_angle * self.rotation_times)
                surface.blit(rotated_spaceship, (self.position_x, self.position_y))
                self.rotation_times += 1
            else:
                rotated_spaceship = pygame.transform.rotate(spaceship, self.rotation_angle * self.rotation_times)
                surface.blit(rotated_spaceship, (self.position_x, self.position_y))
        else:
            surface.blit(spaceship, (self.position_x, self.position_y))
    
    def move(self, surface, level_completed):
        if not level_completed:
            if pygame.key.get_pressed()[pygame.K_UP] and self.position_y > 0:
                self.position_y -= self.speed
            if pygame.key.get_pressed()[pygame.K_DOWN] and self.position_y < (surface.get_height() - SPACESHIP_IMAGE_HEIGHT):
                self.position_y += self.speed
        else:
            arrived = False
            movement = 0
            if self.position_y < SCREEN_HEIGHT/2 - SPACESHIP_IMAGE_HEIGHT/2:
                self.position_y += 1
                movement += 1
            if self.position_y > SCREEN_HEIGHT/2 - SPACESHIP_IMAGE_HEIGHT/2:
                self.position_y -= 1
                movement += 1
            if self.position_x < SCREEN_WIDTH - PLANET_IMAGES_WIDTH/2 - SPACESHIP_IMAGE_WIDTH/2:
                self.position_x += 2
                movement += 1
            if movement == 0:
                arrived = True
            self.rotate = True
            return arrived
    
    def score_crash_verification(self, obstacles, level_completed):
        crash = False
        game_over = False
        new_obstacle = obstacles
        for index, obstacle in enumerate(obstacles):
            if obstacle.position_x + obstacle.image_width <= 0:
                self.score += 1
                new_obstacle.pop(index)
            if not level_completed:
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