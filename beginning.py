import pygame

from tools import BEGINNING_SOUND, BLANCO, FONT_20, FONT_30, FONT_60, SCREEN_BACKGROUND_BEGINNING


class Beginning():

    def __init__(self, screen):

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background_image_path = SCREEN_BACKGROUND_BEGINNING
        self.sound = pygame.mixer.Sound(BEGINNING_SOUND)
    
    def screen_loop(self):

        finished = False

        while not finished:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                finished = True
                pygame.mixer.quit()
                return True
            
            pygame.mixer.init()
            self.sound.play(-1)
            background = pygame.image.load(self.background_image_path)
            self.screen.blit(background, (0, 0))

            title = FONT_60.render("THE QUEST FOR LIFE", True, BLANCO)
            self.screen.blit(title, (15, 100))

            explanation = ["The earth is dying and", "we will go find a new planet", "to survive."]
            for i, text in enumerate(explanation):
                surface = FONT_20.render(text, True, BLANCO)
                self.screen.blit(surface, (100, 260 + (20 * i)))
            
            instructions = ["You will need to use the top and down arrows", "in your keyboard to move the spaceship", "and avoid the dangers."]
            for i, text in enumerate(instructions):
                surface = FONT_20.render(text, True, BLANCO)
                self.screen.blit(surface, (200, 400 + (20 * i)))
    
            begin = ["Press enter to begin", "this adventure or... :)"]
            for i, text in enumerate(begin):
                surface = FONT_30.render(text, True, BLANCO)
                self.screen.blit(surface, (420 + (20 * i), 550 + (20 * (i * 2))))

            pygame.display.flip()
