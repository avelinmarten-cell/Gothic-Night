import pygame
import random
import math

# ==========================================
#         GOTHIC NIGHT — PYTHON
# ==========================================

pygame.init()

WIDTH = 1000
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gothic Night")

clock = pygame.time.Clock()

# ------------------------------------------
# Цвета
# ------------------------------------------

BLACK = (8, 7, 11)
DARK_PURPLE = (25, 15, 30)
BURGUNDY = (90, 20, 45)
LIGHT_BURGUNDY = (150, 45, 70)
PALE = (190, 175, 190)

# ------------------------------------------
# Частицы
# ------------------------------------------

particles = []

for _ in range(90):
    particles.append({
        "x": random.uniform(0, WIDTH),
        "y": random.uniform(0, HEIGHT),
        "size": random.uniform(0.5, 2.0),
        "speed": random.uniform(0.08, 0.35),
        "phase": random.uniform(0, math.pi * 2),
        "alpha": random.randint(40, 130)
    })

# ------------------------------------------
# Создание мягкого свечения
# ------------------------------------------

def create_glow(radius, color, alpha):

    surface = pygame.Surface(
        (radius * 2, radius * 2),
        pygame.SRCALPHA
    )

    center = radius

    for r in range(radius, 0, -4):

        current_alpha = int(
            alpha * (1 - r / radius) ** 2
        )

        pygame.draw.circle(
            surface,
            (*color, current_alpha),
            (center, center),
            r
        )

    return surface

# ------------------------------------------
# Луна
# ------------------------------------------

moon_glow = create_glow(
    130,
    (120, 35, 65),
    55
)

# ------------------------------------------
# Главный цикл
# ------------------------------------------

running = True
time = 0

while running:

    dt = clock.tick(60) / 1000
    time += dt

    # --------------------------------------
    # Выход
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # --------------------------------------
    # Фон
    # --------------------------------------

    screen.fill(BLACK)

    # Очень мягкий вертикальный градиент

    for y in range(HEIGHT):

        progress = y / HEIGHT

        r = int(8 + 10 * progress)
        g = int(7 + 4 * progress)
        b = int(11 + 15 * progress)

        pygame.draw.line(
            screen,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )

    # --------------------------------------
    # Центральное свечение
    # --------------------------------------

    glow = create_glow(
        300,
        (75, 15, 40),
        35
    )

    screen.blit(
        glow,
        (
            WIDTH // 2 - 300,
            HEIGHT // 2 - 300
        )
    )

    # --------------------------------------
    # Луна
    # --------------------------------------

    moon_x = WIDTH // 2
    moon_y = 210

    screen.blit(
        moon_glow,
        (
            moon_x - 130,
            moon_y - 130
        )
    )

    # Основной круг луны

    pygame.draw.circle(
        screen,
        (175, 165, 175),
        (moon_x, moon_y),
        48
    )

    # Затемняем часть луны,
    # создавая тонкий серп

    pygame.draw.circle(
        screen,
        (12, 10, 16),
        (moon_x + 18, moon_y - 8),
        48
    )

    # --------------------------------------
    # Частицы
    # --------------------------------------

    for particle in particles:

        particle["y"] -= particle["speed"]

        particle["x"] += math.sin(
            time * 0.6 + particle["phase"]
        ) * 0.08

        # Если частица ушла вверх —
        # возвращаем её вниз

        if particle["y"] < -5:

            particle["y"] = HEIGHT + 5
            particle["x"] = random.uniform(0, WIDTH)

        # Мягкое мерцание

        pulse = (
            math.sin(
                time * 1.5 + particle["phase"]
            ) + 1
        ) / 2

        alpha = int(
            particle["alpha"] * (0.5 + pulse * 0.5)
        )

        particle_surface = pygame.Surface(
            (8, 8),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            particle_surface,
            (*PALE, alpha),
            (4, 4),
            particle["size"]
        )

        screen.blit(
            particle_surface,
            (
                int(particle["x"]) - 4,
                int(particle["y"]) - 4
            )
        )

    # --------------------------------------
    # Готическая декоративная линия
    # --------------------------------------

    line_y = HEIGHT - 105

    # Центральная линия

    pygame.draw.line(
        screen,
        (70, 25, 45),
        (270, line_y),
        (730, line_y),
        1
    )

    # --------------------------------------
    # Центральный ромб
    # --------------------------------------

    center_x = WIDTH // 2

    diamond = [
        (center_x, line_y - 12),
        (center_x + 12, line_y),
        (center_x, line_y + 12),
        (center_x - 12, line_y)
    ]

    pygame.draw.polygon(
        screen,
        (70, 25, 45),
        diamond,
        1
    )

    # --------------------------------------
    # Маленькие декоративные элементы
    # --------------------------------------

    for offset in (45, -45):

        pygame.draw.circle(
            screen,
            (90, 30, 50),
            (
                center_x + offset,
                line_y
            ),
            3,
            1
        )

    # --------------------------------------
    # Медленное мерцание центра
    # --------------------------------------

    pulse = (
        math.sin(time * 1.2) + 1
    ) / 2

    glow_alpha = int(
        25 + pulse * 30
    )

    small_glow = create_glow(
        90,
        (120, 30, 55),
        glow_alpha
    )
    
    screen.blit(
        small_glow,
        (
            center_x - 90,
            line_y - 90
        )
    )

    # --------------------------------------
    # Обновление экрана
    # --------------------------------------

    pygame.display.flip()

pygame.quit()