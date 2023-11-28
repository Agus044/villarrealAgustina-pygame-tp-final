import pygame as pg
from auxiliar import SurfaceManager as sf
from constantes import *
from caja import Caja

class Personaje:

    def __init__(self, coord_x: int, coord_y: int, frame_rate = 100, speed_walk = 6, gravity = 16, jump = 32):
        """Inicializa una instancia de la clase Personaje.

        Parameters:
        - `coord_x` (int): La coordenada x inicial del personaje.
        - `coord_y` (int): La coordenada y inicial del personaje.
        - `frame_rate` (int): La velocidad de fotogramas de la animación. Default: 100
        - `speed_walk` (int): La velocidad de desplazamiento lateral. Default: 6
        - `gravity` (int): La fuerza de gravedad que afecta al personaje. Default: 16
        - `jump` (int): La potencia del salto del personaje. Default: 32
        """
        self.__iddle_r = sf.get_surface_from_spritesheet('./assets/player/Iddle/player_idle.png', 5, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet('./assets/player/Iddle/player_idle.png', 5, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet('./assets/player/Walk/player_walk.png', 13, 1)
        self.__walk_l = sf.get_surface_from_spritesheet('./assets/player/Walk/player_walk.png', 13, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet('./assets/player/Jump/player_jump.png', 6, 1)
        self.__jump_l = sf.get_surface_from_spritesheet('./assets/player/Jump/player_jump.png', 6, 1, flip=True)
        self.__attack_r = sf.get_surface_from_spritesheet('./assets/player/Attack/Melee/player_atk_melee.png', 10, 1)
        self.__attack_l = sf.get_surface_from_spritesheet('./assets/player/Attack/Melee/player_atk_melee.png', 10, 1, flip=True)
        self.__shoot_r = sf.get_surface_from_spritesheet('./assets/player/Attack/Shoot/player_shoot.png', 14, 1)
        self.__shoot_l = sf.get_surface_from_spritesheet('./assets/player/Attack/Shoot/player_shoot.png', 14, 1, flip=True)
        
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True
        
        self.__vida = 3
        self.__puntos = 0

    
    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        """_summary_

        Args:
            move_x (_type_): _description_
            animation_list (list[pg.surface.Surface]): _description_
            look_r (bool): _description_
        """
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        
    
    def __set_y_animations_preset(self):
        """Configura las propiedades relacionadas con la animación vertical del jugador para el salto.
        """
        self.__move_y = -self.__jump
        self.__move_x = self.__speed_walk if self.__is_looking_right else -self.__speed_walk
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        self.__is_jumping = True
    
    def walk(self, direction: str = 'Right'):
        """Inicia la animación de caminar en la dirección especificada.

        Args:
            direction (str): Dirección del movimiento ('Right' para derecha, 'Left' para izquierda).
        """
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=look_right)
    
    
    def stay(self):
        """Detiene la animación y establece al jugador en un estado de reposo.
        """
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0
    
    def jump(self, jumping: bool):
        """Inicia o detiene la animación de salto del jugador.

        Args:
            jumping (bool): True para iniciar el salto, False para detenerlo.
        """
        if jumping and not self.__is_jumping:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()
    
    def attack(self):
        """Inicia la animación de ataque del personaje.
        """
        if not self.__is_jumping:
            attack_animation = self.__attack_r if self.__is_looking_right else self.__attack_l
            self.__actual_animation = attack_animation
            self.__initial_frame = 0
    
    def shoot(self):
        """Inicia la animación de disparo del personaje.
        """
        if not self.__is_jumping:
            shoot_animation = self.__shoot_r if self.__is_looking_right else self.__shoot_l
            self.__actual_animation = shoot_animation
            self.__initial_frame = 0
    
    def __set_borders_limits(self):
        """Limita el movimiento del jugador dentro de los bordes de la ventana.

        Returns:
            int: Cantidad de píxeles que puede moverse horizontalmente y verticalmente.
        """
        pixels_move_x = 0
        pixels_move_y = 0
        
        if self.__move_x > 0:
            pixels_move_x = self.__move_x if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move_x = self.__move_x if self.__rect.x > 0 else 0
        
        
        if self.__move_y > 0:
            pixels_move_y = self.__move_y if self.__rect.y < ALTO_VENTANA - self.__actual_img_animation.get_height() else 0
        elif self.__move_y < 0:
            pixels_move_y = self.__move_y if self.__rect.y > 0 else 0
        
        return pixels_move_x, pixels_move_y
    
    def check_collision_with_plataformas(self, plataformas):
        """Verifica la colisión del personaje con las plataformas.

        Parameters:
        - `plataformas` (List[Plataforma]): Lista de plataformas en el juego.

        Returns:
        - ([Plataforma]): La plataforma con la cual el personaje colisiona desde arriba, o None si no hay colisión.
        """
        for plataforma in plataformas:
            if self.__rect.colliderect(plataforma.rect) and self.__rect.y < plataforma.rect.y:
                return plataforma
        return None

    def do_movement(self, delta_ms: int, plataformas):
        """Realiza el movimiento del personaje y maneja las colisiones con las plataformas.

        Parameters:
        - `delta_ms` (int): El tiempo transcurrido desde la última actualización en milisegundos.
        - `plataformas` (List[Plataforma]): Lista de plataformas en el juego.
        """
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            pixel_move_x, pixel_move_y = self.__set_borders_limits()
            self.__rect.x += pixel_move_x
            self.__rect.y += pixel_move_y
            
            # Verificar colisiones con las plataformas
            plataforma_colisionada = self.check_collision_with_plataformas(plataformas)

            if plataforma_colisionada:
                # Ajustar la posición del jugador en la plataforma
                self.__rect.y = plataforma_colisionada.rect.y - self.__rect.height
                self.__is_jumping = False
                self.__move_y = 0
            # Parte relacionado a saltar
            if self.__rect.y < 500:
                self.__rect.y += self.__gravity

    def do_animation(self, delta_ms: int):
        """Realiza la animación del personaje.

        Parameters:
        - `delta_ms` (int): El tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                if self.__is_jumping:
                    self.__is_jumping = False
                    self.__move_y = 0
    
    def update(self, delta_ms: int, plataformas):
        """Actualiza el estado del personaje.

        Parameters:
        - `delta_ms` (int): El tiempo transcurrido desde la última actualización en milisegundos.
        - `plataformas` (List[Plataforma]): Lista de plataformas en el juego.
        """
        self.do_movement(delta_ms, plataformas)
        self.do_animation(delta_ms)
    
    def draw(self, screen: pg.surface.Surface):
        """Dibuja el personaje en la pantalla.

        Parameters:
        - `screen` (pg.surface.Surface): Superficie de la pantalla en la que se dibujará el personaje.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
            
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)