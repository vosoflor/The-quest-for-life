import random
import pygame
from obstacles import Obstacles
from spaceship import Spaceship

from tools import BLANCO, EXPLOSION_IMAGE_SEQUENCE, EXPLOSION_SOUND, FONT, GAME_SOUND, SCREEN_BACKGROUND, SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE_HEIGHT


class Game():

    def __init__(self, screen, spaceship: Spaceship) -> None:
        self.screen = screen
        self.background_image_path = SCREEN_BACKGROUND
        self.background_position_x = 0
        self.clock = pygame.time.Clock()
        self.level = 0
        self.level_timer = 20000
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
        position_image_sequence = 0
        explosion_animation_stopwatch = 0

        while not self.game_over and level_stopwatch <= self.level_timer:

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

                self.spaceship.draw(self.screen)
                self.spaceship.move(self.screen)
                
                self.lapse_between_obstacles = random.randint(2000, 6000)

                if between_obstacles >= self.lapse_between_obstacles and level_stopwatch <= self.level_timer:
                    for i in range(0, self.level + 4):
                        self.obstacles_list.append(Obstacles(random.randint(8, 16)))
                    between_obstacles = 0
                
                for obstacle in self.obstacles_list:
                    obstacle.draw(self.screen)
                    obstacle.move()

                score_crash_verification = self.spaceship.score_crash_verification(self.obstacles_list)
                self.crash = score_crash_verification[0]
                self.obstacles_list = score_crash_verification[2]

                between_obstacles += self.clock.get_time()
                level_stopwatch += self.clock.get_time()
                
                if self.background_position_x <= -1 * SCREEN_WIDTH:
                    self.background_position_x = 0
                else:
                    self.background_position_x -= self.spaceship_speed_forward
            
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
                self.game_over = score_crash_verification[1]
            
            game_info = self.font.render(f"Level : {str(self.level + 1)}", True, BLANCO)
            self.screen.blit(game_info, (1050,20))
            game_info = self.font.render(f"Lives   : {str(self.spaceship.lives)}", True, BLANCO)
            self.screen.blit(game_info, (1050,60))
            game_info = self.font.render(f"Score : {str(self.spaceship.score)}", True, BLANCO)
            self.screen.blit(game_info, (40,20))

            pygame.display.flip()

            self.clock.tick(600)
        
        if self.game_over:
            self.lost_level()
        else:
            self.level += 1
            self.level_completed()
    
    def lost_level(self):
        pass

    def level_completed(self):
        pass