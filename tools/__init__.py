import pygame

DATABASE = "data/records.sqlite"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_BACKGROUND = "images/milky-way-1.jpg"
SPACESHIP_IMAGE = "images/spaceship.png"
SPACESHIP_IMAGE_WIDTH = 85
SPACESHIP_IMAGE_HEIGHT = 87
OBSTACLES_TYPES_IMAGES = {"asteroid" : "images/asteroid.png", "meteor" : "images/meteor.png", "meteorite" : "images/meteorite.png"}
EXPLOSION_SOUND= "sounds/boom.mp3"
EXPLOSION_IMAGE_SEQUENCE = ["images/explosion1.png", "images/explosion2.png", "images/explosion3.png"]
FONT = "fonts/SPACE-ARMOR.otf"
GAME_SOUND = "sounds/space-odyssey.mp3"

BLANCO = (255, 255, 255)
VERDE = (0, 128, 94)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

pygame.init()