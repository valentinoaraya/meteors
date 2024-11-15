import pygame, random, sys
import constantes

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ventana = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))
pygame.display.set_caption("Meteors")

# Cargo las imágenes
fondo = pygame.image.load("./images/fondoEspacio.jpg")
fondo = pygame.transform.scale(fondo, (constantes.ANCHO, constantes.ALTO))

naveImagen = pygame.image.load("./images/nave.png")
naveImagen = pygame.transform.scale(naveImagen, (100, 100))

meteoroImagen = pygame.image.load("./images/meteorito.png")
meteoroImagen = pygame.transform.scale(meteoroImagen, (50, 50))

tituloImagen = pygame.image.load("./images/title.png")
tituloImagen = pygame.transform.scale(tituloImagen, (600, 300))

tituloFinJuego = pygame.image.load("./images/finishgame.png")
tituloFinJuego = pygame.transform.scale(tituloFinJuego, (600, 300))

# Fuente texto
fuente = pygame.font.Font(None, 36)

# Puntaje
puntaje = 0


def menuPrincipal():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # Salir del menú y comenzar el juego

        ventana.blit(fondo, (0, 0))
        ventana.blit(
            tituloImagen,
            (
                constantes.ANCHO // 2 - tituloImagen.get_width() // 2,
                constantes.ALTO // 4,
            ),
        )

        textoJugar = fuente.render(
            "Presiona ESPACIO para jugar", True, constantes.BLANCO
        )
        ventana.blit(
            textoJugar,
            (constantes.ANCHO // 2 - textoJugar.get_width() // 2, constantes.ALTO // 2),
        )

        pygame.display.flip()
        pygame.time.Clock().tick(30)


def menuFinJuego():

    global puntaje

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                puntaje = 0
                return  # Salir del menú y comenzar el juego

        ventana.blit(fondo, (0, 0))

        ventana.blit(
            tituloFinJuego,
            (
                constantes.ANCHO // 2 - tituloFinJuego.get_width() // 2,
                constantes.ALTO // 4,
            ),
        )

        textoReiniciar = fuente.render(
            "Presiona ESPACIO para reiniciar", True, constantes.BLANCO
        )
        ventana.blit(
            textoReiniciar,
            (
                constantes.ANCHO // 2 - textoReiniciar.get_width() // 2,
                constantes.ALTO - 200,
            ),
        )

        textoPuntaje = fuente.render(f"PUNTOS: {puntaje}", True, constantes.BLANCO)
        ventana.blit(
            textoPuntaje,
            (
                constantes.ANCHO // 2 - textoPuntaje.get_width() // 2,
                constantes.ALTO - 300,
            ),
        )

        pygame.display.flip()
        pygame.time.Clock().tick(30)


def juego():

    global puntaje

    # Configuración del jugador
    jugador = pygame.Rect(
        constantes.ANCHO // 2, constantes.ALTO - 120, 100, 100
    )  # Posición y tamaño del jugador
    velocidad_jugador = 15

    # Configuración de los meteoritos
    listaMeteoritos = []

    for _ in range(5):
        meteorito = pygame.Rect(random.randint(0, constantes.ANCHO - 20), 0, 50, 50)
        listaMeteoritos.append(meteorito)

    velocidad_objeto = 20
    vidas = 3
    posicionFondo = 0

    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador.left > 0:
            jugador.x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador.right < constantes.ANCHO:
            jugador.x += velocidad_jugador
        if teclas[pygame.K_UP] and jugador.top > 0:
            jugador.y += -velocidad_jugador
        if teclas[pygame.K_DOWN] and jugador.bottom < constantes.ALTO:
            jugador.y += velocidad_jugador

        for meteoro in listaMeteoritos:

            # Movimiento del meteoro
            meteoro.y += velocidad_objeto

            # Comprobar si el objeto llega al fondo
            if meteoro.y > constantes.ALTO:
                meteoro.y = random.randint(-400, -40)
                meteoro.x = random.randint(0, constantes.ANCHO - meteoro.width)
                velocidad_objeto += 0.1
                puntaje += 1
                print(puntaje)

            # Comprobar colisión
            if jugador.colliderect(meteoro):
                vidas -= 1
                print(f"VIDAS: {vidas}")
                meteoro.y = 0
                meteoro.x = random.randint(0, constantes.ANCHO - meteoro.width)

                if vidas <= 0:
                    return  # Salir del juego y mostrar menú de fin del juego

        # Movimiento del fondo
        posicionFondo += 2
        if posicionFondo >= constantes.ALTO:
            posicionFondo = 0

        # Dibujar en pantalla
        ventana.blit(fondo, (0, posicionFondo - constantes.ALTO))
        ventana.blit(fondo, (0, posicionFondo))
        ventana.blit(naveImagen, (jugador.x, jugador.y))
        for meteoro in listaMeteoritos:
            ventana.blit(meteoroImagen, (meteoro.x, meteoro.y))  # Meteoro

        # Mostrar vidas
        textoVidas = fuente.render(f"VIDAS: {vidas}", True, constantes.BLANCO)
        ventana.blit(textoVidas, (10, 10))

        # Mostrar puntaje
        textoPuntaje = fuente.render(f"PUNTOS: {puntaje}", True, constantes.BLANCO)
        ventana.blit(textoPuntaje, (10, 40))

        # Actualizar la pantalla
        pygame.display.flip()
        pygame.time.Clock().tick(30)  # Limitar a 30 FPS


while True:
    menuPrincipal()
    juego()
    menuFinJuego()
