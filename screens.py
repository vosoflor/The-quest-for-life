import random
import pygame
from connection import ConnectDatabase
from objects import Spaceship, Obstacles, Planet
from tools import *


class Beginning():

    def __init__(self, screen):

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background_image_path = SCREEN_BACKGROUND_BEGINNING
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(BEGINNING_SOUND)
    
    def screen_loop(self):
        
        pygame.display.set_caption("Menu: The quest for life :p")

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
        
        pygame.mixer.init()

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
        self.waiting_time = 0
        self.player = True
    
    def start(self):

        pygame.display.set_caption("Game - The quest for life :p")

        while not self.game_over and self.player:

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
                        # Si después de un minuto el jugador no continua el juego entonces vuelve
                        # a pantalla principal
                        self.waiting_time += self.clock.get_time()
                        if self.waiting_time > 60000:
                            self.player = False
                        
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
        self.waiting_time = 0
        self.player = True
        self.start()

class Game_Over():

    def __init__(self, screen) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()

    # Método para mostrar pantalla de game over durante 9 segundos antes de regresar 
    # a pantalla principal
    def print_screen(self):
        
        pygame.display.set_caption("Game Over - The quest for life ;(")

        sound_played = False
        game_over_stopwatch = 0

        while game_over_stopwatch < 3000:

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
            
            game_over_stopwatch += self.clock.get_time()
            self.clock.tick(600)
    
class Positions_Table():

    def __init__(self, screen, game) -> None:
        self.screen = screen
        self.game = game
        self.clock = pygame.time.Clock()
        self.positions_table = []
    
    def check_score(self):
        
        added = False

        connection = ConnectDatabase("SELECT id, name_initials, score FROM positions_table order by score DESC;")
        self.positions_table = connection.select_all()
        input = Name_Initials(self.screen)
        
        if len(self.positions_table) < 5:
            name = input.ask_input()
            connection = ConnectDatabase("INSERT INTO positions_table (name_initials, score) VALUES(?, ?)", (name, self.game.spaceship.score))
            connection.insert()
            added = True
        else:
            for record in self.positions_table:
                if record["score"] < self.game.spaceship.score and not added:
                    name = input.ask_input()
                    connection = ConnectDatabase("INSERT INTO positions_table (name_initials, score) VALUES(?, ?)", (name, self.game.spaceship.score))
                    connection.insert()
                    added = True
        
        connection = ConnectDatabase("SELECT id, name_initials, score FROM positions_table order by score DESC;")
        self.positions_table = connection.select_all()        
        
        if len(self.positions_table) > 5:
            id = self.positions_table[-1]["id"]
            self.positions_table.pop(-1)
            connection = ConnectDatabase(f"DELETE FROM positions_table WHERE id={id}")
            connection.delete_by()
    
    def print(self):

        pygame.display.set_caption("Top 5 !!! - The quest for life :D")

        stopwatch = 0

        while stopwatch < 8000:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.screen.fill(NEGRO)
            
            text_surface = FONT_60.render("¡ BEST PLAYERS !", True, BLANCO)
            self.screen.blit(text_surface, (80, 50))

            for index, record in enumerate(self.positions_table):

                rect = pygame.Rect(250, 80 + ((index+1) * 100), 400, 100)
                pygame.draw.rect(self.screen, BLANCO, rect, 5)
                text_surface = FONT_60.render(record["name_initials"], True, BLANCO)
                self.screen.blit(text_surface, (rect.x + 70, rect.y + 10))
                
                rect = pygame.Rect(650, 80 + ((index+1) * 100), 400, 100)
                pygame.draw.rect(self.screen, BLANCO, rect, 5)
                text_surface = FONT_60.render(str(record["score"]), True, BLANCO)
                self.screen.blit(text_surface, (rect.x + 120, rect.y + 10))

            pygame.display.flip()
            
            self.clock.tick(600)

            stopwatch += self.clock.get_time()

class Name_Initials ():

    def __init__(self, screen) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()

    def ask_input(self):
        
        pygame.display.set_caption("Record top 5 - The quest for life :D")

        typing = True

        player_initials = ""

        input_color = pygame.Color("lightskyblue3")
        input_field = pygame.Rect(500, 400, 300, 100)

        while typing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_initials = player_initials[:-1]
                    else:
                        if len(player_initials) < 3:
                            player_initials += event.unicode
            
            if pygame.key.get_pressed()[pygame.K_c]:
                typing = False

            self.screen.fill(NEGRO)

            message1 = FONT_60.render("You got in top 5", True, BLANCO)
            self.screen.blit(message1, (130, 80))
            message2 = FONT_60.render("type your initials", True, BLANCO)
            self.screen.blit(message2, (70, 160))
            message2 = FONT_60.render("and press c", True, BLANCO)
            self.screen.blit(message2, (240, 240))

            pygame.draw.rect(self.screen, input_color, input_field)
            text_surface = FONT_60.render(player_initials, True, NEGRO)
            self.screen.blit(text_surface, (input_field.x + 22, input_field.y + 7))
            
            message2 = FONT_60.render("To continue", True, BLANCO)
            self.screen.blit(message2, (240, 550))

            pygame.display.flip()
            
            self.clock.tick(600)    
        
        return player_initials

