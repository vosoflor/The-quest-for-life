import pygame

pygame.init()

DATABASE = "data/positions_table.sqlite"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_BACKGROUND = "images/milky-way-1.jpg"
SCREEN_BACKGROUND_BEGINNING = "images/milky-way-2.jpg"
SPACESHIP_IMAGE = "images/spaceship.png"
SPACESHIP_IMAGE_WIDTH = 85
SPACESHIP_IMAGE_HEIGHT = 87
OBSTACLES_TYPES_IMAGES = {"asteroid" : "images/asteroid.png", "meteor" : "images/meteor.png", "meteorite" : "images/meteorite.png"}
EXPLOSION_SOUND= "sounds/boom.mp3"
EXPLOSION_IMAGE_SEQUENCE = ["images/explosion1.png", "images/explosion2.png", "images/explosion3.png"]
FONT = "fonts/SPACE-ARMOR.otf"
FONT_20 = pygame.font.Font(FONT, 20)
FONT_30 = pygame.font.Font(FONT, 30)
FONT_60 = pygame.font.Font(FONT, 60)
GAME_SOUND = "sounds/space-odyssey.mp3"
BEGINNING_SOUND = "sounds/game-thrones.mp3"
PLANET_IMAGES = "images/planet1.png"
PLANET_IMAGES_WIDTH = 765
GAME_OVER_SOUND = "sounds/pacman-dies.mp3"

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)