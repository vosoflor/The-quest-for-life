import pygame
from tools import PLANET_IMAGES, PLANET_IMAGES_WIDTH, SCREEN_WIDTH


class Planet:
    
    def __init__(self) -> None:
        
        self.planet_image_path = PLANET_IMAGES
        self.planet_position_x = SCREEN_WIDTH
    
    def draw(self, screen):
        
        planet = pygame.image.load(self.planet_image_path)
        screen.blit(planet, (self.planet_position_x, 0))
        if self.planet_position_x > SCREEN_WIDTH - PLANET_IMAGES_WIDTH/2:
            self.planet_position_x -= 4