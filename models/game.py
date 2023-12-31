import pygame
import sys
from constantes import *
from menus import *
from nivel import cargar_nivel
from ranking import *

class Game:
    def __init__(self) -> None:
        """Inicializa un objeto Game
        """
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Star Wars Ep. III")
        self.clock = pygame.time.Clock()
        self.PAUSA = False
        self.cronometro = 60 * 1000
        self.iniciar_nivel = False
        self.nivel_actual = 0
        self.puntos_acumulados = 0
        self.game_over = False
        
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/sounds/main_theme.mp3")
        pygame.mixer.music.play(-1)
        
        self.font = pygame.font.Font(None, 36)
        
        self.anakin = None
        self.plataformas = None
        self.cajas = None
        self.enemigos = None
        self.bombas = None
        self.balas_enemigas = None
        
        crear_tabla_ranking()
    
    def handle_events(self):
        """Maneja los eventos del juego, respondiendo a las teclas presionadas o liberadas.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Estoy cerrando el juego")
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.PAUSA = not self.PAUSA
                else:
                    self.anakin.handle_events([event])
    
    def iniciar_juego(self, nivel):
        """Inicializara el nivel del juego seleccionado
        
        Args:
            nivel (int): nivel especifico del juego
        """
        self.iniciar_nivel = True
        
        match nivel:
            case 1:
                self.anakin, self.plataformas, self.cajas, self.fondo, self.enemigos, self.bombas = cargar_nivel("nivel1.json")
                self.bg = pygame.image.load(self.fondo)
                self.bg = pygame.transform.scale(self.bg, (ANCHO_VENTANA, ALTO_VENTANA))
                self.cronometro = 60 * 1000
                self.nivel_actual = 1
            case 2:
                self.anakin, self.plataformas, self.cajas, self.fondo, self.enemigos, self.bombas = cargar_nivel("nivel2.json")
                self.bg = pygame.image.load(self.fondo)
                self.bg = pygame.transform.scale(self.bg, (ANCHO_VENTANA, ALTO_VENTANA))
                self.cronometro = 60 * 1000
                self.nivel_actual = 2
            case 3:
                self.anakin, self.plataformas, self.cajas, self.fondo, self.enemigos, self.bombas = cargar_nivel("nivel3.json")
                self.bg = pygame.image.load(self.fondo)
                self.bg = pygame.transform.scale(self.bg, (ANCHO_VENTANA, ALTO_VENTANA))
                self.cronometro = 60 * 1000
                self.nivel_actual = 3
    
    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje en el centro de la pantalla durante un breve período.
        
        Args:
            mensaje (str): El mensaje que se mostrará en la pantalla.
        """
        text = self.font.render(mensaje, True, WHITE)
        self.screen.blit(text, (ANCHO_VENTANA // 2 - text.get_width() // 2, ALTO_VENTANA // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000) 
    
    def verificar_condiciones(self):
        """Verifica las condiciones del juego para determinar si de debe
        avanzar a otro nivel, mostrar el mensaje de victoria o game over, y
        actualizar el ranking.
        """
        if self.nivel_actual == 3 and len(self.cajas) == 0 and len(self.enemigos) == 0:
            # En el último nivel y todas las cajas y enemigos eliminados
            self.game_over = True
            self.iniciar_nivel = False
            self.mostrar_mensaje("¡Victoria!")

            if self.puntos_acumulados > 0:
                # Pide al jugador su nombre para la tabla de ranking
                nombre_jugador = input("Ingresa tu nombre: ")
                
                agregar_puntuacion(nombre_jugador, self.puntos_acumulados)
                ranking = obtener_ranking()
                mostrar_pantalla_ranking(self.screen, ranking)

        elif len(self.cajas) == 0 and len(self.enemigos) == 0:
            # Avanzar al siguiente nivel si se cumplen las condiciones
            self.puntos_acumulados += self.anakin.get_puntos()
            self.nivel_actual += 1
            self.iniciar_nivel = False
            self.iniciar_juego(self.nivel_actual)
    
    def mostrar_ranking(self):
        """Muestra la pantalla de ranking en la ventana del juego.
        """
        ranking = obtener_ranking()
        
        mostrar_pantalla_ranking(self.screen, ranking)
    
    def handle_key_input(self):
        """Maneja la entrada del teclado para el juego.

        Captura el estado de las teclas presionadas y llama al método `handle_key_input`
        del objeto `anakin` para procesar la entrada del personaje.
        """
        keys = pygame.key.get_pressed()
        self.anakin.handle_key_input(keys, pygame.time.get_ticks())

    def update(self):
        """Actualiza el estado del juego.
        Calcula el tiempo transcurrido desde la última actualización, 
        llama al método `update` del objeto `anakin` para actualizar su estado,
        las plataformas, los enemigos, las cajas y las bombas.
        """
        delta_ms = self.clock.tick(FPS)
        
        if self.iniciar_nivel:
            self.cronometro -= delta_ms
            
            if self.cronometro <= 0:
                self.game_over = True
                self.iniciar_nivel = False
        
        self.enemigos.update(delta_ms, self.plataformas.sprites())
        self.anakin.update(delta_ms, self.plataformas.sprites(), self.enemigos, self.cajas, self.bombas)
        
        if self.anakin.get_vida() <= 0:
            self.game_over = True
            self.iniciar_nivel = False
        
        self.verificar_condiciones()
        ranking = obtener_ranking()
        
        if self.game_over:
            self.mostrar_mensaje("Game Over")
            menu_principal(self.screen, self.iniciar_juego, ranking)
            self.game_over = False
    
    def draw(self):
        """Dibuja los elementos del juego en la pantalla.
        
        Rellena la pantalla con un color de fondo, dibuja el fondo y luego
        dibuja las plataformas, cajas, enemigos y el personaje (`anakin`).
        """
        self.screen.fill(BLACK)
        self.screen.blit(self.bg, self.bg.get_rect())
        
        self.plataformas.draw(self.screen)
        self.cajas.draw(self.screen)
        self.enemigos.draw(self.screen)
        self.bombas.draw(self.screen)
        self.anakin.draw(self.screen)
        
        # Dibujar la puntuación en la pantalla
        puntuacion_texto = f"Puntuación: {self.puntos_acumulados + self.anakin.get_puntos()}"
        texto_puntuacion = self.font.render(puntuacion_texto, True, WHITE)
        self.screen.blit(texto_puntuacion, (ANCHO_VENTANA - texto_puntuacion.get_width() - 10, 10))
        
        # Dibujar las vidas en la pantalla
        vidas_texto = f"Vidas: {self.anakin.get_vida()}"
        texto_vidas = self.font.render(vidas_texto, True, WHITE)
        self.screen.blit(texto_vidas, (10, 50))
        
        # Dibujar el cronómetro en la pantalla
        minutos = int(self.cronometro / 60000)
        segundos = int((self.cronometro % 60000) / 1000)
        tiempo_texto = f"{minutos:02}:{segundos:02}"
        texto = self.font.render(tiempo_texto, True, WHITE)
        self.screen.blit(texto, (10, 10))
        
        pygame.display.update()
    
    def run(self):
        """Inicia la ejecución del juego.
        
        Muestra el menú principal y luego ejecuta un bucle principal del juego.
        Dentro del bucle, maneja eventos, procesa la entrada del teclado, actualiza
        el estado del juego y dibuja los elementos en la pantalla
        """
        ranking = obtener_ranking()
        menu_principal(self.screen, self.iniciar_juego, ranking)
        
        while EJECUTANDO:
            self.handle_events()
            
            if self.PAUSA:
                pausar_juego(self.screen, [self.PAUSA])
                self.PAUSA = False
                
            self.handle_key_input()
            self.update()
            self.draw()
        
        sys.exit()