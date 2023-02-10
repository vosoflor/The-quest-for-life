import random
import pygame
from obstacles import Obstacles

from spaceship import Spaceship
from tools import SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
game_over = False
between_obstacles = 0
level_stopwatch = 0
explosion_animation_timer = 0
crash = False
score = 0
x1 = 0
x2 = 1280
y = 0
x = 0

spaceship = Spaceship(screen.get_height()/2 - SPACESHIP_IMAGE_HEIGHT/2)
obstacles_list = []

while not game_over:
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

    if not crash:

        spaceship.draw(screen)
        spaceship.move(screen)
    
        if between_obstacles >= 1000 and level_stopwatch <= 20000:
            obstacles_list.append(Obstacles(random.randint(5,10)))
            between_obstacles = 0
        
        for obstacle in obstacles_list:
            obstacle.draw(screen)
            obstacle.move()

        crash_verification = spaceship.crash_verification(obstacles_list)
        crash = crash_verification[0]

        obstacles_list = spaceship.add_to_score(obstacles_list)

        between_obstacles += clock.get_time()
        level_stopwatch += clock.get_time()
    
    else:
      
        pygame.mixer.init()
        explosion = pygame.mixer.Sound("sounds/boom.mp3")
        explosion.play(-1)
        explosion_sequence = ["explosion1.png", "explosion2.png", "explosion3.png"]
        explosion = pygame.image.load(f"images/{explosion_sequence[x]}")
        screen.blit(explosion, (spaceship.position_x, spaceship.position_y))
        if x == 2:
            x = 0
        else:
            x += 1
        explosion_animation_timer += clock.get_time()
    
    if explosion_animation_timer >= 3000:
        pygame.mixer.quit()
        explosion_animation_timer = 0
        crash = False
        spaceship.position_y = screen.get_height()/2 - SPACESHIP_IMAGE_HEIGHT/2
        obstacles_list = []
        game_over = crash_verification[1]

    if x1 <= -1280:
        x1 = 0
        x2 = 1280
    else:
        x1 -= 5
        x2 -= 5
        
    # Render the graphics here.
    # ...

    pygame.display.flip()  # Refresh on-screen display

    clock.tick(600)         # wait until next frame (at 60 FPS)