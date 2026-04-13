import pygame
import math

pygame.init()

# Screen setup
W, H = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Grid settings
cols, rows = 50, 30
spacing = 20

points = []
sticks = []

# Create grid points
for y in range(rows):
    for x in range(cols):
        px = x * spacing + (W // 2 - cols * spacing // 2)
        py = y * spacing + (H // 2 - rows * spacing // 2)
        points.append([px, py, px, py, False])  # x, y, oldx, oldy, locked

# Create sticks (connections)
def index(x, y):
    return y * cols + x

for y in range(rows):
    for x in range(cols):
        if x < cols - 1:
            sticks.append([index(x, y), index(x+1, y)])
        if y < rows - 1:
            sticks.append([index(x, y), index(x, y+1)])

running = True
while running:
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update points (Verlet integration)
    for p in points:
        if not p[4]:  # not locked
            vx = (p[0] - p[2]) * 0.99
            vy = (p[1] - p[3]) * 0.99

            p[2], p[3] = p[0], p[1]
            p[0] += vx
            p[1] += vy

            # Mouse interaction (attraction)
            if mouse_pressed:
                dx = p[0] - mx
                dy = p[1] - my
                dist = math.hypot(dx, dy)
                if dist < 80:
                    p[0] = mx + dx * 0.5
                    p[1] = my + dy * 0.5

    # Stick constraints
    for _ in range(5):
        for s in sticks:
            p1 = points[s[0]]
            p2 = points[s[1]]

            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue

            diff = (dist - spacing) / dist
            offsetx = dx * 0.5 * diff
            offsety = dy * 0.5 * diff

            if not p1[4]:
                p1[0] += offsetx
                p1[1] += offsety
            if not p2[4]:
                p2[0] -= offsetx
                p2[1] -= offsety

    # Draw grid
    for s in sticks:
        p1 = points[s[0]]
        p2 = points[s[1]]
        pygame.draw.line(screen, (0, 255, 150), (p1[0], p1[1]), (p2[0], p2[1]), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()