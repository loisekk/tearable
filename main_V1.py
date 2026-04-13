import pygame
import math
import random

pygame.init()

info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Cloth Simulation")
clock = pygame.time.Clock()

COLS, ROWS = 40, 25
REST = 18
GRAVITY = 0.5
DAMPING = 0.99
ITERATIONS = 5
TEAR_DIST = REST * 2.8
CUT_RADIUS = 28

def lerp_color(t):
    t = max(0.0, min(1.0, t))
    r = int(30 + t * 220)
    g = int(220 - t * 180)
    b = int(80 - t * 70)
    return (r, g, b)

points = []
sticks = []

def index(x, y):
    return y * COLS + x

def reset_sim():
    global points, sticks
    points = []
    sticks = []
    ox = (W - (COLS - 1) * REST) // 2
    oy = 60
    for y in range(ROWS):
        for x in range(COLS):
            px = ox + x * REST
            py = oy + y * REST
            locked = (y == 0 and x % 4 == 0)
            points.append({
                'x': float(px), 'y': float(py),
                'ox': float(px), 'oy': float(py),
                'locked': locked
            })
    for y in range(ROWS):
        for x in range(COLS):
            if x < COLS - 1:
                sticks.append([index(x, y), index(x+1, y), REST, False])
            if y < ROWS - 1:
                sticks.append([index(x, y), index(x, y+1), REST, False])

reset_sim()

wind_on = False
wind_force = 0.0
mode = 'drag'  # 'drag' or 'cut'

font = pygame.font.SysFont("monospace", 16)

running = True
while running:
    clock.tick(60)
    screen.fill((10, 10, 20))

    mx, my = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    left_down = mouse_buttons[0]
    right_down = mouse_buttons[2]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                reset_sim()
            if event.key == pygame.K_w:
                wind_on = not wind_on
            if event.key == pygame.K_c:
                mode = 'cut' if mode == 'drag' else 'drag'

    # Wind
    if wind_on:
        t = pygame.time.get_ticks() / 1000.0
        wind_force = math.sin(t * 1.0) * 0.6 + math.cos(t * 0.7) * 0.4

    # Update points
    for p in points:
        if p['locked']:
            continue

        vx = (p['x'] - p['ox']) * DAMPING
        vy = (p['y'] - p['oy']) * DAMPING

        p['ox'] = p['x']
        p['oy'] = p['y']

        p['x'] += vx + (wind_force if wind_on else 0.0)
        p['y'] += vy + GRAVITY

        # Left click: drag/attract
        if left_down and mode == 'drag':
            dx = p['x'] - mx
            dy = p['y'] - my
            dist = math.hypot(dx, dy)
            if dist < 80:
                p['x'] = mx + dx * 0.5
                p['y'] = my + dy * 0.5

        # Boundary collisions
        if p['x'] < 0:
            p['x'] = 0
            p['ox'] = p['x'] + vx * 0.3
        if p['x'] > W:
            p['x'] = float(W)
            p['ox'] = p['x'] + vx * 0.3
        if p['y'] < 0:
            p['y'] = 0
            p['oy'] = p['y'] + vy * 0.3
        if p['y'] > H:
            p['y'] = float(H)
            p['oy'] = p['y'] + vy * 0.3

    # Stick constraints
    for _ in range(ITERATIONS):
        for s in sticks:
            if s[3]:
                continue
            p1 = points[s[0]]
            p2 = points[s[1]]
            dx = p2['x'] - p1['x']
            dy = p2['y'] - p1['y']
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue

            # Auto-tear if stretched too far
            if dist > TEAR_DIST:
                s[3] = True
                continue

            diff = (dist - s[2]) / dist * 0.5
            ox = dx * diff
            oy = dy * diff

            if not p1['locked']:
                p1['x'] += ox
                p1['y'] += oy
            if not p2['locked']:
                p2['x'] -= ox
                p2['y'] -= oy

    # Cut mode: right-click or cut mode + left-click tears sticks
    if right_down or (mode == 'cut' and left_down):
        for s in sticks:
            if s[3]:
                continue
            p1 = points[s[0]]
            p2 = points[s[1]]
            cx = (p1['x'] + p2['x']) / 2
            cy = (p1['y'] + p2['y']) / 2
            if math.hypot(cx - mx, cy - my) < CUT_RADIUS:
                s[3] = True

    # Draw sticks
    for s in sticks:
        if s[3]:
            continue
        p1 = points[s[0]]
        p2 = points[s[1]]
        dx = p2['x'] - p1['x']
        dy = p2['y'] - p1['y']
        stretch = math.hypot(dx, dy) / s[2] - 1
        color = lerp_color(stretch * 4)
        pygame.draw.line(screen, color,
                         (int(p1['x']), int(p1['y'])),
                         (int(p2['x']), int(p2['y'])), 1)

    # Draw locked anchor points
    for p in points:
        if p['locked']:
            pygame.draw.circle(screen, (255, 255, 255),
                               (int(p['x']), int(p['y'])), 3)

    # HUD
    hud = [
        f"R = Reset  |  W = Wind {'ON' if wind_on else 'OFF'}  |  C = Mode: {mode.upper()}",
        "Left click: drag cloth   Right click: tear cloth",
        f"FPS: {int(clock.get_fps())}"
    ]
    for i, line in enumerate(hud):
        surf = font.render(line, True, (180, 180, 200))
        screen.blit(surf, (14, 14 + i * 20))

    pygame.display.flip()

pygame.quit()