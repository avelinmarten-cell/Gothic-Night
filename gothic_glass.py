import pygame
import random
import math

pygame.init()

# ==================================================
# WINDOW
# ==================================================

WIDTH, HEIGHT = 900, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gothic Stained Glass")

clock = pygame.time.Clock()

# ==================================================
# COLORS
# ==================================================

BACKGROUND_TOP = (6, 5, 9)
BACKGROUND_BOTTOM = (17, 11, 20)

FRAME_DARK = (20, 15, 23)
FRAME_LIGHT = (55, 40, 55)

GLASS_COLORS = [
    (91, 31, 57),     # burgundy
    (69, 34, 79),     # muted purple
    (38, 47, 75),     # midnight blue
    (108, 49, 66),    # ruby
    (56, 42, 73),     # violet
    (78, 35, 49)      # wine
]

MOONLIGHT = (190, 177, 198)

# ==================================================
# BACKGROUND
# ==================================================

background = pygame.Surface((WIDTH, HEIGHT))

for y in range(HEIGHT):

    t = y / HEIGHT

    r = int(
        BACKGROUND_TOP[0] +
        (BACKGROUND_BOTTOM[0] - BACKGROUND_TOP[0]) * t
    )

    g = int(
        BACKGROUND_TOP[1] +
        (BACKGROUND_BOTTOM[1] - BACKGROUND_TOP[1]) * t
    )

    b = int(
        BACKGROUND_TOP[2] +
        (BACKGROUND_BOTTOM[2] - BACKGROUND_TOP[2]) * t
    )

    pygame.draw.line(
        background,
        (r, g, b),
        (0, y),
        (WIDTH, y)
    )

# ==================================================
# GLOW FUNCTION
# ==================================================

def create_glow(radius, color, alpha):

    surface = pygame.Surface(
        (radius * 2, radius * 2),
        pygame.SRCALPHA
    )

    center = radius

    for r in range(radius, 0, -5):

        strength = int(
            alpha * (1 - r / radius) ** 2
        )

        pygame.draw.circle(
            surface,
            (*color, strength),
            (center, center),
            r
        )

    return surface

# Large atmospheric glow
ambient_glow = create_glow(
    340,
    (91, 39, 82),
    32
)

# Soft moonlight
moon_glow = create_glow(
    270,
    (185, 170, 195),
    28
)

# ==================================================
# VITRAZH POSITION
# ==================================================

CX = WIDTH // 2
CY = HEIGHT // 2 - 35

ARCH_WIDTH = 440
ARCH_HEIGHT = 500

OUTER_RADIUS = 215
INNER_RADIUS = 78

# ==================================================
# GOTHIC ARCH
# ==================================================

def gothic_arch(cx, cy, width, height):

    left = cx - width // 2
    right = cx + width // 2

    top = cy - height // 2
    bottom = cy + height // 2

    points = [
        (left, bottom),
        (left, cy),

        (left + width * 0.12, cy - height * 0.32),

        (cx, top),

        (right - width * 0.12, cy - height * 0.32),

        (right, cy),
        (right, bottom)
    ]

    return points

outer_arch = gothic_arch(
    CX,
    CY,
    ARCH_WIDTH,
    ARCH_HEIGHT
)

inner_arch = gothic_arch(
    CX,
    CY,
    ARCH_WIDTH - 22,
    ARCH_HEIGHT - 22
)

# ==================================================
# GLASS SURFACE
# ==================================================

glass = pygame.Surface(
    (WIDTH, HEIGHT),
    pygame.SRCALPHA
)

# ==================================================
# CENTRAL ROSE
# ==================================================

rose_center = (CX, CY + 10)

PETALS = 8

for i in range(PETALS):

    angle = (
        i *
        math.pi * 2 /
        PETALS
    )

    next_angle = (
        angle +
        math.pi / PETALS
    )

    outer1 = (
        CX +
        math.cos(angle) *
        INNER_RADIUS,

        rose_center[1] +
        math.sin(angle) *
        INNER_RADIUS
    )

    outer2 = (
        CX +
        math.cos(angle + math.pi / PETALS * 2) *
        INNER_RADIUS,

        rose_center[1] +
        math.sin(angle + math.pi / PETALS * 2) *
        INNER_RADIUS
    )

    inner = (
        CX +
        math.cos(next_angle) * 38,

        rose_center[1] +
        math.sin(next_angle) * 38
    )

    pygame.draw.polygon(
        glass,
        (*GLASS_COLORS[i % len(GLASS_COLORS)], 185),
        [
            rose_center,
            outer1,
            inner,
            outer2
        ]
    )

# ==================================================
# RADIAL GLASS
# ==================================================

SEGMENTS = 12

for i in range(SEGMENTS):

    angle1 = (
        i *
        math.pi * 2 /
        SEGMENTS
    )

    angle2 = (
        (i + 1) *
        math.pi * 2 /
        SEGMENTS
    )

    inner1 = (
        CX +
        math.cos(angle1) *
        INNER_RADIUS,

        rose_center[1] +
        math.sin(angle1) *
        INNER_RADIUS
    )

    inner2 = (
        CX +
        math.cos(angle2) *
        INNER_RADIUS,

        rose_center[1] +
        math.sin(angle2) *
        INNER_RADIUS
    )

    outer1 = (
        CX +
        math.cos(angle1) *
        OUTER_RADIUS,

        rose_center[1] +
        math.sin(angle1) *
        OUTER_RADIUS
    )

    outer2 = (
        CX +
        math.cos(angle2) *
        OUTER_RADIUS,

        rose_center[1] +
        math.sin(angle2) *
        OUTER_RADIUS
    )

    pygame.draw.polygon(
        glass,
        (*GLASS_COLORS[(i + 2) % len(GLASS_COLORS)], 175),
        [
            inner1,
            inner2,
            outer2,
            outer1
        ]
    )

# ==================================================
# SIDE PANELS
# ==================================================

left_panel = [
    (CX - 215, CY + 190),
    (CX - 215, CY - 30),
    (CX - 115, CY - 135),
    (CX - 95, CY + 190)
]

right_panel = [
    (CX + 215, CY + 190),
    (CX + 215, CY - 30),
    (CX + 115, CY - 135),
    (CX + 95, CY + 190)
]

pygame.draw.polygon(
    glass,
    (64, 29, 67, 170),
    left_panel
)

pygame.draw.polygon(
    glass,
    (38, 43, 70, 170),
    right_panel
)

# ==================================================
# SMALL GLASS HIGHLIGHTS
# ==================================================

for _ in range(28):

    x = random.randint(
        CX - 195,
        CX + 195
    )

    y = random.randint(
        CY - 170,
        CY + 180
    )

    pygame.draw.circle(
        glass,
        (
            210,
            195,
            210,
            random.randint(25, 70)
        ),
        (x, y),
        random.choice([1, 1, 2])
    )

# ==================================================
# PARTICLES
# ==================================================

particles = []

for _ in range(55):

    particles.append({
        "x": random.randint(100, WIDTH - 100),
        "y": random.randint(70, HEIGHT - 80),
        "speed": random.uniform(0.08, 0.3),
        "size": random.choice([1, 1, 1, 2]),
        "phase": random.uniform(
            0,
            math.pi * 2
        )
    })

# ==================================================
# MOON REFLECTIONS
# ==================================================

reflections = []

for _ in range(7):

    reflections.append({
        "x": random.randint(
            CX - 180,
            CX + 180
        ),

        "y": random.randint(
            CY - 160,
            CY + 170
        ),

        "size": random.randint(
            20,
            45
        ),

        "speed": random.uniform(
            0.08,
            0.22
        ),

        "phase": random.uniform(
            0,
            math.pi * 2
        )
    })

# ==================================================
# DECORATIVE LINE
# OUR SIGNATURE
# ==================================================

def draw_decorative_line(surface, y):

    center = WIDTH // 2

    # Main line
    pygame.draw.line(
        surface,
        (92, 66, 91),
        (center - 250, y),
        (center + 250, y),
        1
    )

    # Central ornament
    pygame.draw.circle(
        surface,
        (150, 112, 145),
        (center, y),
        3
    )

    pygame.draw.circle(
        surface,
        (48, 34, 50),
        (center, y),
        7,
        1
    )

    # Side diamonds
    for offset in (-170, 170):

        x = center + offset

        points = [
            (x, y - 4),
(x + 5, y),
            (x, y + 4),
            (x - 5, y)
        ]

        pygame.draw.polygon(
            surface,
            (112, 82, 108),
            points
        )

    # End details
    pygame.draw.line(
        surface,
        (92, 66, 91),
        (center - 250, y - 4),
        (center - 250, y + 4),
        1
    )

    pygame.draw.line(
        surface,
        (92, 66, 91),
        (center + 250, y - 4),
        (center + 250, y + 4),
        1
    )

# ==================================================
# MAIN LOOP
# ==================================================

running = True
time = 0

while running:

    clock.tick(60)

    time += 0.02

    # ------------------------------------------------
    # EVENTS
    # ------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # ------------------------------------------------
    # BACKGROUND
    # ------------------------------------------------

    screen.blit(
        background,
        (0, 0)
    )

    # ------------------------------------------------
    # AMBIENT GLOW
    # ------------------------------------------------

    pulse = (
        math.sin(time * 1.1) + 1
    ) / 2

    glow_alpha = int(
        18 + pulse * 10
    )

    soft_glow = create_glow(
        330,
        (91, 39, 82),
        glow_alpha
    )

    screen.blit(
        soft_glow,
        (
            CX - soft_glow.get_width() // 2,
            CY - soft_glow.get_height() // 2
        )
    )

    # ------------------------------------------------
    # GLASS
    # ------------------------------------------------

    screen.blit(
        glass,
        (0, 0)
    )

    # ------------------------------------------------
    # SOFT MOONLIGHT
    # ------------------------------------------------

    screen.blit(
        moon_glow,
        (
            CX - moon_glow.get_width() // 2,
            CY - moon_glow.get_height() // 2
        )
    )

    # ------------------------------------------------
    # MOON REFLECTIONS
    # ------------------------------------------------

    reflection_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    for reflection in reflections:

        reflection["x"] += reflection["speed"]

        reflection["y"] += (
            math.sin(
                time * 0.7 +
                reflection["phase"]
            ) * 0.06
        )

        if reflection["x"] > CX + 215:

            reflection["x"] = CX - 215

        length = (
            reflection["size"] * 2.2
        )

        alpha = int(
            7 +
            7 *
            (
                math.sin(
                    time * 1.2 +
                    reflection["phase"]
                ) + 1
            ) / 2
        )

        pygame.draw.ellipse(
            reflection_surface,
            (
                220,
                210,
                225,
                alpha
            ),
            (
                int(
                    reflection["x"] -
                    length / 2
                ),

                int(
                    reflection["y"] - 3
                ),

                int(length),
                6
            )
        )

    screen.blit(
        reflection_surface,
        (0, 0)
    )

    # ------------------------------------------------
    # FLOATING PARTICLES
    # ------------------------------------------------

    for particle in particles:

        particle["y"] -= (
            particle["speed"]
        )

        particle["x"] += (
            math.sin(
                time +
                particle["phase"]
            ) * 0.12
        )

        if particle["y"] < 60:

            particle["y"] = HEIGHT - 80

            particle["x"] = random.randint(
                100,
                WIDTH - 100
            )

        alpha = int(
            35 +
            25 *
            (
                math.sin(
                    time * 1.4 +
                    particle["phase"]
                ) + 1
            ) / 2
        )

        pygame.draw.circle(
            screen,
            (
                185,
                155,
                190,
                alpha
            ),
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["size"]
        )

    # ------------------------------------------------
    # GLASS FRAME
    # ------------------------------------------------

    pygame.draw.lines(
        screen,
        FRAME_LIGHT,
        False,
        outer_arch,
        12
    )

    pygame.draw.lines(
        screen,
        FRAME_DARK,
        False,
        outer_arch,
        7
    )

    pygame.draw.lines(
        screen,
        (38, 29, 39),
        False,
        inner_arch,
        4
    )

    # ------------------------------------------------
    # LEADING BETWEEN GLASS
    # ------------------------------------------------

    for i in range(SEGMENTS):

        angle = (
            i *
            math.pi * 2 /
            SEGMENTS
        )

        start = (
            CX,
            rose_center[1]
        )

        end = (
            CX +
            math.cos(angle) *
            OUTER_RADIUS,

            rose_center[1] +
            math.sin(angle) *
            OUTER_RADIUS
        )

        pygame.draw.line(
            screen,
            FRAME_DARK,
            start,
            end,
            5
        )

    # ------------------------------------------------
    # CENTRAL ROSE FRAME
    # ------------------------------------------------

    pygame.draw.circle(
        screen,
        FRAME_DARK,
        rose_center,
        INNER_RADIUS + 3,
        5
    )

    pygame.draw.circle(
        screen,
        FRAME_LIGHT,
        rose_center,
        35,
        4
    )

    # ------------------------------------------------
    # CENTRAL ORNAMENT
    # ------------------------------------------------

    pygame.draw.circle(
        screen,
        FRAME_DARK,
        rose_center,
        9
    )

    pygame.draw.circle(
        screen,
        (100, 72, 102),
        rose_center,
        4
    )

    # ------------------------------------------------
    # SMALL GOTHIC DIAMONDS
    # ------------------------------------------------

    def draw_diamond(x, y, size):

        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y)
        ]

        pygame.draw.polygon(
            screen,
            FRAME_LIGHT,
            points
        )

    draw_diamond(
        CX,
        CY - 205,
        8
    )

    draw_diamond(
        CX,
        CY + 205,
        8
    )

    # ------------------------------------------------
    # TINY MOON SPARKLES
    # ------------------------------------------------

    for i in range(5):

        sparkle_x = int(
            CX +
            math.sin(
                time * 0.35 +
                i * 2.1
            ) * 175
        )

        sparkle_y = int(
            CY +
            math.cos(
                time * 0.27 +
                i * 1.7
            ) * 165
        )

        sparkle_alpha = int(
            30 +
            35 *
            (
                math.sin(
                    time * 1.5 +
                    i
                ) + 1
            ) / 2
        )

        pygame.draw.circle(
            screen,
            (
                215,
                205,
                220,
                sparkle_alpha
            ),
            (
                sparkle_x,
                sparkle_y
            ),
            1
        )

    # ------------------------------------------------
    # SIGNATURE DECORATIVE LINE
    # ------------------------------------------------

    draw_decorative_line(
        screen,
        HEIGHT - 55
    )

    # ------------------------------------------------
    # DISPLAY
    # ------------------------------------------------

    pygame.display.flip()

pygame.quit()