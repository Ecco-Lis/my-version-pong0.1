import pygame
import random

# Definir los colores personalizados (en formato RGB)
COLOR_OBJETOS = (255, 0, 0)  # Rojo
COLOR_FONDO = (0, 0, 0)      # Negro

# Dimensiones de la ventana del juego
ANCHO = 600
ALTO = 400

# Dimensiones de las paletas
ANCHO_PALA = 10
ALTO_PALA = 80

class Pong:
    def __init__(self):
        """
        Inicializa la instancia del juego Pong.
        Configura la pantalla, la pelota, las paletas y el reloj del juego.
        """
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Pong")
        self.reloj = pygame.time.Clock()
        
        # Inicializar la pelota en el centro y establecer su velocidad inicial de forma aleatoria
        self.pelota = pygame.Rect(ANCHO // 2 - 10, ALTO // 2 - 10, 20, 20)
        self.velocidad_pelota = [random.choice((1, -1)) * 5, random.choice((1, -1)) * 5]

        # Inicializar las paletas en posiciones iniciales
        self.jugador1 = pygame.Rect(10, ALTO // 2 - ALTO_PALA // 2, ANCHO_PALA, ALTO_PALA)
        self.jugador2 = pygame.Rect(ANCHO - 20, ALTO // 2 - ALTO_PALA // 2, ANCHO_PALA, ALTO_PALA)

        # Contadores de puntos para cada jugador
        self.puntos_jugador1 = 0
        self.puntos_jugador2 = 0

    def mover_pelota(self):
        """
        Mueve la pelota y controla su rebote en los bordes y en las paletas.
        """
        self.pelota.x += self.velocidad_pelota[0]
        self.pelota.y += self.velocidad_pelota[1]

        # Rebotar la pelota en los bordes superior e inferior
        if self.pelota.top <= 0 or self.pelota.bottom >= ALTO:
            self.velocidad_pelota[1] = -self.velocidad_pelota[1]

        # Rebotar la pelota en las paletas y contar puntos
        if self.pelota.colliderect(self.jugador1):
            self.velocidad_pelota[0] = abs(self.velocidad_pelota[0])
            self.puntos_jugador1 += 1
        elif self.pelota.colliderect(self.jugador2):
            self.velocidad_pelota[0] = -abs(self.velocidad_pelota[0])
            self.puntos_jugador2 += 1

        # Reiniciar la pelota en el centro si sale de la pantalla
        if self.pelota.left < 0 or self.pelota.right > ANCHO:
            self.pelota.x = ANCHO // 2 - 10
            self.pelota.y = ALTO // 2 - 10
            self.velocidad_pelota = [random.choice((1, -1)) * 5, random.choice((1, -1)) * 5]

    def jugar(self):
        """
        Función principal que ejecuta el juego Pong.
        Controla el movimiento de las paletas de los jugadores y actualiza la pantalla.
        """
        salir = False
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    salir = True

            teclas = pygame.key.get_pressed()

            # Control de movimiento para el jugador 1 (izquierda)
            if teclas[pygame.K_w] and self.jugador1.top > 0:
                self.jugador1.y -= 5
            if teclas[pygame.K_s] and self.jugador1.bottom < ALTO:
                self.jugador1.y += 5

            # Control de movimiento para el jugador 2 (derecha)
            if teclas[pygame.K_UP] and self.jugador2.top > 0:
                self.jugador2.y -= 5
            if teclas[pygame.K_DOWN] and self.jugador2.bottom < ALTO:
                self.jugador2.y += 5

            self.mover_pelota()

            # Dibujar la pantalla y los objetos
            pygame.draw.rect(self.pantalla, COLOR_FONDO, ((0, 0), (ANCHO, ALTO)))
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, self.jugador1)
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, self.jugador2)
            pygame.draw.ellipse(self.pantalla, COLOR_OBJETOS, self.pelota)

            # Mostrar los puntos en pantalla
            font = pygame.font.Font(None, 36)
            puntos_texto = font.render(f"{self.puntos_jugador1} - {self.puntos_jugador2}", True, COLOR_OBJETOS)
            self.pantalla.blit(puntos_texto, (ANCHO // 2 - puntos_texto.get_width() // 2, 10))

            pygame.display.flip()

            self.reloj.tick(60)

        pygame.quit()

if __name__ == '__main__':
    juego = Pong()
    juego.jugar()
