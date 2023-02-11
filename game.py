import random
import pygame
from obstacles import Obstacles
from planet import Planet
from spaceship import Spaceship

from tools import BLANCO, EXPLOSION_IMAGE_SEQUENCE, EXPLOSION_SOUND, FONT_20, FONT_30, GAME_SOUND, SCREEN_BACKGROUND, SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE_HEIGHT


class Game:

    def __init__(self, screen, spaceship: Spaceship) -> None:
        self.screen = screen
        self.background_image_path = SCREEN_BACKGROUND
        self.background_position_x = 0
        self.clock = pygame.time.Clock()
        self.level = 0
        self.level_timer = 10000
        self.spaceship = spaceship
        self.planet = Planet()
        self.obstacles_list = []
        self.lapse_between_obstacles = 200
        self.crash = False
        self.explosion_animation_timer = 3000
        self.game_over = False
        self.sound = pygame.mixer.Sound(GAME_SOUND)
    
    def start(self):

        between_obstacles = 0
        level_stopwatch = 0
        level_completed = False
        position_image_sequence = 0
        explosion_animation_stopwatch = 0
        arrived = False

        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.music_and_background(arrived, self.crash)

            if not self.crash:
                
                arrived = self.spaceship.move(self.screen, level_completed)
                level_completed = level_stopwatch > self.level_timer

                if level_completed:
                    self.planet.draw(self.screen)
                
                else:
                    self.lapse_between_obstacles = 1000 - 200 * self.level
                    if between_obstacles >= self.lapse_between_obstacles:
                        self.obstacles_list.append(Obstacles(random.randint(8, 16)))
                        between_obstacles = 0
                
                for obstacle in self.obstacles_list:
                    obstacle.draw(self.screen)
                    obstacle.move()
        
                self.spaceship.draw(self.screen)

                if arrived:
                    self.next_level_instructions()

                score_crash_verification = self.spaceship.score_crash_verification(self.obstacles_list, level_completed)
                
                self.crash = score_crash_verification[0]
                self.game_over = score_crash_verification[1]
                self.obstacles_list = score_crash_verification[2]

                between_obstacles += self.clock.get_time()
                level_stopwatch += self.clock.get_time()
            
            else:

                result = self.crash_animation(position_image_sequence, explosion_animation_stopwatch)
                position_image_sequence = result[0]
                explosion_animation_stopwatch = result[1]

            self.render_game_info()

            pygame.display.flip()

            self.clock.tick(600)
        
        pygame.mixer.quit()


    def music_and_background(self, arrived, crash):
        pygame.mixer.init()
        self.sound.play(-1)
        background = pygame.image.load(self.background_image_path)
        self.screen.blit(background, (self.background_position_x, 0))
        self.screen.blit(background, (self.background_position_x + SCREEN_WIDTH, 0))
        if not (arrived or crash):
            if self.background_position_x <= -1 * SCREEN_WIDTH:
                self.background_position_x = 0
            else:
                self.background_position_x -= 5
    
    def next_level_instructions(self):
        self.sound.stop()
        next_level_text = ["Press ENTER to get", "the next level :D"]
        surface = FONT_30.render(next_level_text[0], True, BLANCO)
        self.screen.blit(surface, (230, SCREEN_HEIGHT/2 - 100))
        surface = FONT_30.render(next_level_text[1], True, BLANCO)
        self.screen.blit(surface, (260, SCREEN_HEIGHT/2 + 50))

    def crash_animation(self, position_image_sequence, explosion_animation_stopwatch):
        self.sound.stop()
        pygame.mixer.Sound(EXPLOSION_SOUND).play(-1)
        explosion_image = pygame.image.load(EXPLOSION_IMAGE_SEQUENCE[position_image_sequence])
        self.screen.blit(explosion_image, (self.spaceship.position_x, self.spaceship.position_y))
        if explosion_animation_stopwatch%1 == 0:
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
                obstacle.position_x += 200

        return [position_image_sequence, explosion_animation_stopwatch]
    
    def render_game_info(self):
        game_info = FONT_20.render(f"Level : {str(self.level + 1)}", True, BLANCO)
        self.screen.blit(game_info, (1050,20))
        game_info = FONT_20.render(f"Lives   : {str(self.spaceship.lives)}", True, BLANCO)
        self.screen.blit(game_info, (1050,60))
        game_info = FONT_20.render(f"Score : {str(self.spaceship.score)}", True, BLANCO)
        self.screen.blit(game_info, (40,20))

