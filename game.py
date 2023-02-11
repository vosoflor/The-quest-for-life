import random
import pygame
from obstacles import Obstacles
from spaceship import Spaceship

from tools import BLANCO, EXPLOSION_IMAGE_SEQUENCE, EXPLOSION_SOUND, FONT, GAME_SOUND, PLANET_IMAGES, PLANET_IMAGES_WIDTH, SCREEN_BACKGROUND, SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE_HEIGHT


class Game():

    def __init__(self, screen, spaceship: Spaceship) -> None:
        self.screen = screen
        self.background_image_path = SCREEN_BACKGROUND
        self.planet_image_path = PLANET_IMAGES
        self.planet_position_x = SCREEN_WIDTH
        self.background_position_x = 0
        self.clock = pygame.time.Clock()
        self.level = 0
        self.level_timer = 10500
        self.spaceship = spaceship
        self.spaceship_speed_forward = 5
        self.obstacles_list = []
        self.lapse_between_obstacles = 200
        self.crash = False
        self.explosion_animation_timer = 3000
        self.game_over = False
        self.font = pygame.font.Font(FONT, 20)
        self.sound = pygame.mixer.Sound(GAME_SOUND)
    
    def start_level(self):

        between_obstacles = 0
        level_stopwatch = 0
        level_completed = False
        position_image_sequence = 0
        explosion_animation_stopwatch = 0

        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            pygame.mixer.init()
            self.sound.play(-1)
            background = pygame.image.load(self.background_image_path)
            self.screen.blit(background, (self.background_position_x, 0))
            self.screen.blit(background, (self.background_position_x + SCREEN_WIDTH, 0))

            if not self.crash:

                level_completed = level_stopwatch > self.level_timer

                if level_completed:
                    planet = pygame.image.load(self.planet_image_path)
                    self.screen.blit(planet, (self.planet_position_x, 0))
                    if self.planet_position_x > SCREEN_WIDTH - PLANET_IMAGES_WIDTH/2:
                        self.planet_position_x -= 4
                
                else:
                    self.lapse_between_obstacles = random.randint(2000, 6000)
                    if between_obstacles >= self.lapse_between_obstacles:
                        for i in range(0, self.level + 4):
                            self.obstacles_list.append(Obstacles(random.randint(8, 16)))
                        between_obstacles = 0
                
                for obstacle in self.obstacles_list:
                    obstacle.draw(self.screen)
                    obstacle.move()
                
                arrived = self.spaceship.move(self.screen, level_completed)
                self.spaceship.draw(self.screen)
                if not arrived:
                    if self.background_position_x <= -1 * SCREEN_WIDTH:
                        self.background_position_x = 0
                    else:
                        self.background_position_x -= self.spaceship_speed_forward
                else:
                    self.background_position_x = self.background_position_x
                    self.sound.stop()
                    next_level1 = self.font.render("Pulsa ENTER para continuar", True, BLANCO)
                    self.screen.blit(next_level1, (200, SCREEN_HEIGHT/2 - 100))
                    next_level2 = self.font.render("con el siguiente nivel", True, BLANCO)
                    self.screen.blit(next_level2, (200, SCREEN_HEIGHT/2 + 20))

                score_crash_verification = self.spaceship.score_crash_verification(self.obstacles_list, level_completed)
                self.crash = score_crash_verification[0]
                self.obstacles_list = score_crash_verification[2]

                between_obstacles += self.clock.get_time()
                level_stopwatch += self.clock.get_time()
            
            else:
                self.sound.stop()
                pygame.mixer.Sound(EXPLOSION_SOUND).play(-1)
                explosion_image = pygame.image.load(EXPLOSION_IMAGE_SEQUENCE[position_image_sequence])
                self.screen.blit(explosion_image, (self.spaceship.position_x, self.spaceship.position_y))
                if position_image_sequence < len(EXPLOSION_IMAGE_SEQUENCE) - 1:
                    position_image_sequence += 1
                else:
                    position_image_sequence = 0
                explosion_animation_stopwatch += self.clock.get_time()
            
            if explosion_animation_stopwatch >= self.explosion_animation_timer:
                pygame.mixer.quit()
                explosion_animation_stopwatch = 0
                self.crash = False
                self.spaceship.position_y = self.screen.get_height()/2 - SPACESHIP_IMAGE_HEIGHT/2
                for obstacle in self.obstacles_list:
                    obstacle.position_x += 400
                #self.game_over = score_crash_verification[1]
            
            game_info = self.font.render(f"Level : {str(self.level + 1)}", True, BLANCO)
            self.screen.blit(game_info, (1050,20))
            game_info = self.font.render(f"Lives   : {str(self.spaceship.lives)}", True, BLANCO)
            self.screen.blit(game_info, (1050,60))
            game_info = self.font.render(f"Score : {str(self.spaceship.score)}", True, BLANCO)
            self.screen.blit(game_info, (40,20))

            if level_completed:
                pass

            pygame.display.flip()

            self.clock.tick(600)
        
        if self.game_over:
            self.lost_level()
        else:
            self.level_completed()
    
    def lost_level(self):
        pass

    def level_completed(self):
        self.level += 1
        self.spaceship.score += 10