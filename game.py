import random
import pygame
from obstacles import Obstacles
from planet import Planet
from spaceship import Spaceship

from tools import BLANCO, EXPLOSION_IMAGE_SEQUENCE, EXPLOSION_SOUND, FONT_20, FONT_30, FONT_60, GAME_OVER_SOUND, GAME_SOUND, NEGRO, SCREEN_BACKGROUND, SCREEN_WIDTH, SPACESHIP_IMAGE_HEIGHT, SPACESHIP_IMAGE_WIDTH


class Game:

    def __init__(self, screen, spaceship: Spaceship):

        pygame.mixer.init()       
        self.screen = screen
        self.background_position_x = 0
        self.clock = pygame.time.Clock()
        self.level = 0
        self.level_timer = 21000
        self.spaceship = spaceship
        self.planet = Planet()
        self.obstacles_list = []
        self.lapse_between_obstacles = 0
        self.crash = False
        self.explosion_animation_timer = 800
        self.game_over = False
        self.sound = pygame.mixer.Sound(GAME_SOUND)
        self.end_level_points = 10
        self.end_level_points_given = False
        self.between_obstacles = 0
        self.level_stopwatch = 0
        self.level_completed = False
        self.explosion_animation_stopwatch = 0
        self.position_image_sequence = 0
    
    def start(self):

        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.music_and_background()
            
            # Actividades a realizar mientras no haya colisión
            if not self.crash:
                
                # Utiliza método de la nave para mover y guarda en variable la información de 
                # retorno (si llegó a un planeta nuevo o no)
                self.spaceship.move(self.screen, self.level_completed)

                # Utiliza método propio para asignar puntuación y verificar colisiones
                self.score_crash_verification()

                # Definir variable booleana que indica si el nivel se completó (por tiempo)
                self.level_completed = self.level_stopwatch > self.level_timer

                # Si se alcanzó el fin del nivel imprime planeta y revisa cuando haya aterrizado
                # para inicializar las variables para el siguiente nivel... de lo contrario sigue 
                # generando obstáculos de acuerdo a los parámetros de juego y dificultad
                if self.level_completed:
                    self.planet.draw(self.screen)
                    if self.spaceship.arrived:  
                        self.next_level_instructions()
                        if pygame.key.get_pressed()[pygame.K_RETURN]:
                            self.init_next_level()
                else:
                    self.lapse_between_obstacles = 1000 - 100 * (self.level + 1)
                    if self.between_obstacles >= self.lapse_between_obstacles:
                        self.obstacles_list.append(Obstacles(random.randint(6 * (self.level + 1), 14 * (self.level + 1))))
                        self.between_obstacles = 0
                
                # Imprime obstáculos y los mueve para siguiente iteración
                for obstacle in self.obstacles_list:
                    obstacle.draw(self.screen)
                    obstacle.move()
                
                # Imprime nave
                self.spaceship.draw(self.screen)
                
                # Actualiza cronómetros
                self.between_obstacles += self.clock.get_time()
                self.level_stopwatch += self.clock.get_time()
            
            # Ejecuta animación de colisión con método propio
            else:
                self.crash_animation()

            # Utiliza método propio para imprimir vidas, nivel y puntaje
            self.render_game_info()

            pygame.display.flip()

            self.clock.tick(600)

        pygame.mixer.quit()

        # Utiliza método propio para mostrar pantalla de game over
        self.game_over_screen()

    # Método que inicializa sonido y dibuja pantalla de juego concediendo movimiento a la 
    # imagen de fondo y controlando cuándo se debe detener dicho movimiento
    def music_and_background(self):
        
        # Sonido
        pygame.mixer.init()
        self.sound.play(-1)

        # Imprime 2 copias de la imagen de fondo de pantalla para poder darle movimiento
        background = pygame.image.load(SCREEN_BACKGROUND)
        self.screen.blit(background, (self.background_position_x, 0))
        self.screen.blit(background, (self.background_position_x + SCREEN_WIDTH, 0))

        # Mientras que no haya aterrizado en un planeta o se haya estrellado, la función
        # mueve la posición del fondo para dar percepción de movimiento o en caso contrario
        # detiene el sonido juego
        if not (self.spaceship.arrived or self.crash):
            if self.background_position_x <= -1 * SCREEN_WIDTH:
                self.background_position_x = 0
            else:
                self.background_position_x -= 5
        else:
            self.sound.stop()
    
    # Función que hace el rendering del mensaje de final de nivel e instrucciones 
    # para continuar el juego
    def next_level_instructions(self):

        next_level_text = ["Press ENTER to get", "the next level :D"]
        for index, text in enumerate(next_level_text):
            info = FONT_30.render(text, True, BLANCO)
            self.screen.blit(info, (230 + index * 30, 260 + index * 150))

    # Método para procesar la animación de colisión entre la nave y cualquier obstáculo antes 
    # de finalizar el nivel
    def crash_animation(self):
        
        # Sonido explosión
        pygame.mixer.Sound(EXPLOSION_SOUND).play(-1)

        # Impresión imágen asociada a explosión y actualización índice secuencia
        explosion_image = pygame.image.load(EXPLOSION_IMAGE_SEQUENCE[self.position_image_sequence])
        self.screen.blit(explosion_image, (self.spaceship.position_x, self.spaceship.position_y))
        
        if self.position_image_sequence < len(EXPLOSION_IMAGE_SEQUENCE) - 1:
            self.position_image_sequence += 1
        else:
            self.position_image_sequence = 0
        
        # Identifica si ya transcurrió el tiempo asignado a la animación de colisión y en ese caso
        # termina el sonido, inicializa variable de colisión, reubica la nave y retrasa la posición de 
        # los obstáculos activos para poder reinicar el juego
        if self.explosion_animation_stopwatch >= self.explosion_animation_timer:

            pygame.mixer.quit()
            self.explosion_animation_stopwatch = 0
            self.crash = False
            self.spaceship.position_y = self.screen.get_height()/2 - SPACESHIP_IMAGE_HEIGHT/2
            for obstacle in self.obstacles_list:
                obstacle.position_x += 200

        else:
            self.explosion_animation_stopwatch += self.clock.get_time()
    
    # Método para imprimir en pantalla el nivel, las vidas y el puntaje
    def render_game_info(self):

        game_info = FONT_20.render(f"Level : {str(self.level + 1)}", True, BLANCO)
        self.screen.blit(game_info, (1050,20))
        game_info = FONT_20.render(f"Lives   : {str(self.spaceship.lives)}", True, BLANCO)
        self.screen.blit(game_info, (1050,60))
        game_info = FONT_20.render(f"Score : {str(self.spaceship.score)}", True, BLANCO)
        self.screen.blit(game_info, (40,20))
    
    # Método para mostrar pantalla de game over durante 9 segundos antes de regresar 
    # a pantalla principal
    def game_over_screen(self):
        
        sound_played = False
        game_over_stopwatch = 0

        while game_over_stopwatch < 90000:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            
            # Ejecuta sonido de derrota una vez
            if not sound_played:
                pygame.mixer.init()
                pygame.mixer.Sound(GAME_OVER_SOUND).play(0)
                sound_played = True
            
            # Hace render de GAME OVER en pantalla negra
            self.screen.fill(NEGRO)
            game_over_message = FONT_60.render("GAME OVER", True, BLANCO)
            self.screen.blit(game_over_message, (300,300))    
            pygame.display.flip()

            # Actualiza cronómetro de pantalla game over
            game_over_stopwatch += self.clock.get_time()

    # Método que verifica puntuación obtenida y colisiones con la nave: informa al juego si hubo 
    # colisión, si la nave se quedó sin vidas y ajusta lista de objetos obstáculos eliminando 
    # aquellos objetos que salieron de la pantalla
    def score_crash_verification(self):

        for index, obstacle in enumerate(self.obstacles_list):

            # Revisa si el obstáculo salió de pantalla, asigna punto en caso afirmativo 
            # y elimina el objeto de la lista recibida
            if obstacle.position_x + obstacle.image_width <= 0:
                self.spaceship.score += 1
                self.obstacles_list.pop(index)

            # Mientras no se haya completado el nivel, la función revisa si se cruza 
            # la superficie de la nave con el obstáculo y en caso afirmativo confirma colisión
            # y quita una vida, cuando las vidas son igual a cero informa fin del juego
            if not self.level_completed:

                if (self.spaceship.position_x + SPACESHIP_IMAGE_WIDTH >= obstacle.position_x and
                obstacle.position_x + obstacle.image_width >= self.spaceship.position_x and
                self.spaceship.position_y + SPACESHIP_IMAGE_HEIGHT >= obstacle.position_y and
                obstacle.position_y + obstacle.image_width >= self.spaceship.position_y):
                    
                    self.crash = True
                    self.spaceship.lives -= 1
                    self.obstacles_list.pop(index)

                    if self.spaceship.lives == 0:
                        self.game_over = True
            
            # Cuando el nivel se completa se asignan puntos adicionales al jugador
            else:
                if not self.end_level_points_given:
                    self.spaceship.score += self.end_level_points
                    self.end_level_points_given = True

    # Inicialización de variables para nuevo nivel
    def init_next_level(self):

        self.level += 1
        self.spaceship.position_x = 0
        self.spaceship.rotation_times = 1
        self.spaceship.rotate = False
        self.spaceship.arrived = False
        self.end_level_points_given = False
        self.between_obstacles = 0
        self.level_stopwatch = 0
        self.level_completed = False
        self.explosion_animation_stopwatch = 0
        self.start()
