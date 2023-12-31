import pygame
from constantes import *
from boton import Boton

def pausar_juego(screen, paused):
    """Pausa el juego y muestra una pantalla de pausa.
    
    Args:
        screen (pygame.Surface): La superficie de la pantalla del juego.
        paused (bool): Indica si el juego está actualmente en estado pausado.
    """
    paused = True
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        fondo_pausa = pygame.image.load("./assets/background/bg_pausa.jpeg")
        fondo_pausa = pygame.transform.scale(fondo_pausa, (ANCHO_VENTANA, ALTO_VENTANA))
        screen.blit(fondo_pausa, (0, 0))
        
        fuente = pygame.font.Font(None, 36)
        
        texto1 = fuente.render("JUEGO PAUSADO. Presiona 'C' para continuar o 'Q' para salir.", True, WHITE)
        texto2 = fuente.render("You can now hear the Tragedy of Darth Plagueis, the Wise", True, WHITE)
        
        texto_rect1 = texto1.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        texto_rect2 = texto2.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 3))
        
        screen.blit(texto1, texto_rect1)
        screen.blit(texto2, texto_rect2)
        
        pygame.display.flip()

def menu_opciones(screen, musica_activada=True):
    """Muestra y gestiona el menú de opciones del juego.
    
    Muestra un fondo de menú, botones para activar/desactivar la música y volver al menú principal.
    Permite al usuario interactuar con los botones y realiza acciones correspondientes.
    
    Args:
        screen (pygame.Surface): La superficie de la pantalla del juego.
        musica_activada (bool): Indica si la música está activada o no.
        
    Returns:
        bool: True si el usuario vuelve al menú principal, False de lo contrario.
    """
    fondo_opciones = pygame.image.load("./assets/background/menu_principal.jpg")
    fondo_opciones = pygame.transform.scale(fondo_opciones, (ANCHO_VENTANA, ALTO_VENTANA))
    
    musica_on_boton = Boton(150, 200, 200, 50, "Música: Activada", MAGENTA, (200, 200, 0))
    musica_off_boton = Boton(150, 300, 200, 50, "Música: Desactivada", MAGENTA, (200, 200, 0))
    volver_boton = Boton(150, 500, 200, 50, "Volver", MAGENTA, (200, 200, 200))
    
    en_menu_opciones = True
    en_menu_principal = False
    
    while en_menu_opciones and not en_menu_principal:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                musica_on_boton.handle_event(event)
                musica_off_boton.handle_event(event)
                volver_boton.handle_event(event)
        
        screen.blit(fondo_opciones, (0, 0))
        
        font = pygame.font.Font(None, 36)
        
        
        musica_on_boton.draw(screen, font)
        musica_off_boton.draw(screen, font)
        volver_boton.draw(screen, font)
        
        pygame.display.update()
        
        # Comprobar acciones de los botones del submenú de música
        if musica_on_boton.hovered and pygame.mouse.get_pressed()[0]:
            musica_activada = True
            pygame.mixer.music.unpause()
        elif musica_off_boton.hovered and pygame.mouse.get_pressed()[0]:
            musica_activada = not musica_activada
            pygame.mixer.music.pause()
        elif volver_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu_opciones = False
            en_menu_principal = True
            
    return en_menu_principal


def menu_principal(screen, iniciar_juego, ranking):
    """Muestra y gestiona el menú principal del juego.
    
    Muestra un fondo de menú, botones para iniciar el juego, salir y acceder al menú de opciones.
    Permite al usuario interactuar con los botones y realiza acciones correspondientes.
    
    Args:
        screen (pygame.Surface): La superficie de la pantalla del juego.
        iniciar_juego (callable): Función que inicia el juego.
    """
    fondo_menu = pygame.image.load("./assets/background/menu_principal.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO_VENTANA, ALTO_VENTANA))
    
    iniciar_boton = Boton(150, 200, 200, 50, "Iniciar Juego", BLUE, RED)
    salir_boton = Boton(150, 300, 200, 50, "Salir", RED, BLUE)
    opcion_boton = Boton(150, 400, 200, 50, "Opciones", GREEN, WHITE)
    ranking_boton = Boton(400, 300, 200, 50, "Tabla de ranking", MAGENTA, GREEN)
    niveles_boton = Boton(400, 400, 200, 50, "Seleccionar niveles", YELLOW, RED)
    
    en_menu = True
    
    while en_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                iniciar_boton.handle_event(event)
                salir_boton.handle_event(event)
                opcion_boton.handle_event(event)
                ranking_boton.handle_event(event)
                niveles_boton.handle_event(event)
        
        screen.blit(fondo_menu, (0, 0))
        
        font = pygame.font.Font(None, 36)
        iniciar_boton.draw(screen, font)
        salir_boton.draw(screen, font)
        opcion_boton.draw(screen, font)
        ranking_boton.draw(screen, font)
        niveles_boton.draw(screen, font)
        
        pygame.display.update()
        
        if iniciar_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu = False
            pygame.mixer.music.stop()
            iniciar_juego(1)
            pygame.mixer.music.load("./assets/sounds/stage_music.mp3")
            pygame.mixer.music.play(-1)
        elif salir_boton.hovered and pygame.mouse.get_pressed()[0]:
            pygame.quit()
            quit()
        elif ranking_boton.hovered and pygame.mouse.get_pressed()[0]:
            mostrar_pantalla_ranking(screen, ranking)
        elif niveles_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu = seleccionar_niveles(screen, iniciar_juego)
        elif opcion_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu = menu_opciones(screen, False)
            
            if not en_menu:
                en_menu = True

def mostrar_pantalla_ranking(screen, ranking):
    """Muestra la pantalla de ranking en la ventana del juego.

    Args:
        screen (pygame.Surface): La superficie de la ventana del juego.
        ranking (list): Una lista de tuplas que contiene la información del ranking,
            donde cada tupla tiene el nombre del jugador y su puntuación.
    """
    screen.fill(BLACK)
    
    font = pygame.font.Font(None, 36)
    texto_titulo = font.render("Ranking", True, WHITE)
    screen.blit(texto_titulo, (ANCHO_VENTANA // 2 - texto_titulo.get_width() // 2, 50))

    y_pos = 150
    for i, (jugador, puntuacion) in enumerate(ranking, start=1):
        texto = f"{i}. {jugador}: {puntuacion} puntos"
        texto_ranking = font.render(texto, True, WHITE)
        screen.blit(texto_ranking, (ANCHO_VENTANA // 2 - texto_ranking.get_width() // 2, y_pos))
        y_pos += 40

    pygame.display.flip()

    # Esperar hasta que el jugador presione una tecla para continuar
    esperar_tecla()

def esperar_tecla():
    """Espera a que el jugador presione una tecla antes de continuar.
    """
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                esperando = False

def seleccionar_niveles(screen, iniciar_juego):
    """Sub-menú para seleccionar niveles del juego.

    Permite al usuario elegir en qué nivel desea comenzar a jugar.

    Args:
        screen (pygame.Surface): La superficie de la pantalla del juego.
        iniciar_juego (callable): Función que inicia el juego.
        nivel_actual (int): Nivel actual seleccionado.

    Returns:
        bool: True si el usuario vuelve al menú principal, False de lo contrario.
    """
    fondo_niveles = pygame.image.load("./assets/background/bg_niveles.jpg")
    fondo_niveles = pygame.transform.scale(fondo_niveles, (ANCHO_VENTANA, ALTO_VENTANA))
    
    nivel1_boton = Boton(150, 200, 200, 50, "Nivel 1", BLUE, RED)
    nivel2_boton = Boton(150, 300, 200, 50, "Nivel 2", RED, GREEN)
    nivel3_boton = Boton(150, 400, 200, 50, "Nivel 3", GREEN, BLUE)
    volver_boton = Boton(150, 500, 200, 50, "Volver", YELLOW, MAGENTA)
    
    en_menu_niveles = True
    en_menu_principal = False
    
    while en_menu_niveles and not en_menu_principal:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                nivel1_boton.handle_event(event)
                nivel2_boton.handle_event(event)
                nivel3_boton.handle_event(event)
                volver_boton.handle_event(event)
                
        screen.blit(fondo_niveles, (0, 0))
        font = pygame.font.Font(None, 36)
        nivel1_boton.draw(screen, font)
        nivel2_boton.draw(screen, font)
        nivel3_boton.draw(screen, font)
        volver_boton.draw(screen, font)
        
        pygame.display.update()
        
        if nivel1_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu_niveles = False
            en_menu_principal = False
            iniciar_juego(1)
            pygame.mixer.music.load("./assets/sounds/stage_music.mp3")
            pygame.mixer.music.play(-1)
        elif nivel2_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu_niveles = False
            en_menu_principal = False
            iniciar_juego(2)
            pygame.mixer.music.load("./assets/sounds/stage_music.mp3")
            pygame.mixer.music.play(-1)
        elif nivel3_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu_niveles = False
            en_menu_principal = False
            iniciar_juego(3)
            pygame.mixer.music.load("./assets/sounds/stage_music.mp3")
            pygame.mixer.music.play(-1)
        elif volver_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu_niveles = False
            en_menu_principal = True

    return en_menu_principal