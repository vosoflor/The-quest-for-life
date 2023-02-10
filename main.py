import pygame

from spaceship import Spaceship
from tools import SPACESHIP_IMAGE_HEIGHT

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()
time = 0
x1 = 0
x2 = 1280
x3 = 1280
x4 = 1280
x5 = 1280
y = 0

spaceship = Spaceship(screen.get_height()/2 - SPACESHIP_IMAGE_HEIGHT/2)
meteorite = pygame.image.load("images/meteorite.png")
asteroid = pygame.image.load("images/asteroid.png")
meteor = pygame.image.load("images/meteor.png")


while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    # ...


    background = pygame.image.load("images/milky-way-1.jpg")
    screen.blit(background, (x1, y))
    screen.blit(background, (x2, y))

    spaceship.draw(screen)
    spaceship.move(screen)

    new_meteorite = pygame.transform.scale(meteorite, (100,100))
    new_asteroid = pygame.transform.scale(asteroid, (80,80))
    new_meteor = pygame.transform.scale(meteor, (30,30))
    screen.blit(new_meteorite, (x3, 200))
    screen.blit(new_asteroid, (x4, 500))
    screen.blit(new_meteor, (x5, 600))

    if x1 <= -1280:
        x1 = 0
        x2 = 1280
    else:
        x1 -= 5
        x2 -= 5

    x3 -= 10
    x4 -= 5
    x5 -= 2 

    time += clock.get_time()
    
    # Render the graphics here.
    # ...

    pygame.display.flip()  # Refresh on-screen display

    clock.tick(40)         # wait until next frame (at 60 FPS)