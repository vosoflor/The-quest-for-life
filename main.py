import pygame
from tools import BLANCO, FONT_30, FONT_60, GAME_OVER_SOUND, NEGRO, SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE_HEIGHT
from spaceship import Spaceship
from game import Game

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
spaceship = Spaceship(screen.get_height()/2 - SPACESHIP_IMAGE_HEIGHT/2)
game = Game(screen, spaceship)
game.start()

finish = False

sound_played = False

while not finish:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
            
    if game.game_over:
        if not sound_played:
            pygame.mixer.init()
            game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)
            game_over_sound.play(0)
            sound_played = True
        screen.fill(NEGRO)
        game_over_message = FONT_60.render("GAME OVER", True, BLANCO)
        screen.blit(game_over_message, (290,160))    
        game_over_message = FONT_30.render("PRESS ENTER", True, BLANCO)
        screen.blit(game_over_message, (420,340))    
        game_over_message = FONT_30.render("TO START AGAIN", True, BLANCO)
        screen.blit(game_over_message, (390,440))    
        pygame.display.flip()
