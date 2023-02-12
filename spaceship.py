import pygame
from tools import PLANET_IMAGES_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, SPACESHIP_IMAGE, SPACESHIP_IMAGE_HEIGHT, SPACESHIP_IMAGE_WIDTH

class Spaceship:

    def __init__(self):

        self.image_path = SPACESHIP_IMAGE
        self.position_y = SCREEN_HEIGHT/2 - SPACESHIP_IMAGE_HEIGHT/2
        self.position_x = 0
        self.speed = 18
        self.lives = 3
        self.score = 0
        self.rotate = False
        self.rotation_times = 1
        self.arrived = False
    
    # Método que dibuja la nave, recibe parámetro de pantalla
    def draw(self, screen):

        spaceship = pygame.image.load(self.image_path)

        # Revisa si la variable de rotación está activa para iniciar giro de aterrizaje (180°) en fin de nivel
        if self.rotate:

            rotated_spaceship = pygame.transform.rotate(spaceship, 0.4 * self.rotation_times)
            screen.blit(rotated_spaceship, (self.position_x, self.position_y))

            if self.rotation_times < 450:   
                self.rotation_times += 1

        # Imprime la nave durante el juego mientras no se ha finalizado el nivel
        else:
            screen.blit(spaceship, (self.position_x, self.position_y))
    
    # Método para hacer movimientos de la nave, retorna variable booleana 
    # para indicar cuando la nave ha llegado a un planeta
    def move(self, screen, level_completed):

        # Mientras que el nivel no se haya completado el movimiento lo da el jugador con teclado
        # y con los límites superior e inferior de la pantalla
        if not level_completed:

            if pygame.key.get_pressed()[pygame.K_UP] and self.position_y > 0:
                self.position_y -= self.speed
                
            if (pygame.key.get_pressed()[pygame.K_DOWN] and 
            self.position_y < (screen.get_height() - SPACESHIP_IMAGE_HEIGHT)):
                self.position_y += self.speed
        
        # Cuando el nivel se ha completado el juego toma control y el movimiento de la nave 
        # se hace de forma "automática" acercando la misma al planeta encontrado y "avisando" cuando llega
        else:
            
            self.rotate = True
            movement = 0

            if self.position_y < SCREEN_HEIGHT/2 - SPACESHIP_IMAGE_HEIGHT/2:
                self.position_y += 1
                movement += 1

            if self.position_y > SCREEN_HEIGHT/2 - SPACESHIP_IMAGE_HEIGHT/2:
                self.position_y -= 1
                movement += 1

            if self.position_x < SCREEN_WIDTH - PLANET_IMAGES_WIDTH/2 - SPACESHIP_IMAGE_WIDTH/2:
                self.position_x += 2
                movement += 1

            if movement == 0:
                self.arrived = True