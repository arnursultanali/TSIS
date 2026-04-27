import pygame
import math

def draw_shape(surf, shape_mode, p1, p2, col, th):
    # Calculate normalized coordinates (so you can draw in any direction)
    x, y = min(p1[0], p2[0]), min(p1[1], p2[1])
    w, h = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])

    if shape_mode == 'line':
        pygame.draw.line(surf, col, p1, p2, th)

    elif shape_mode == 'rectangle':
        pygame.draw.rect(surf, col, (x, y, w, h), th)

    elif shape_mode == 'circle':
        # Радиус — расстояние от центра до курсора
        r = int(math.hypot(w, h))
        pygame.draw.circle(surf, col, p1, r, th)

    elif shape_mode == 'square':
        side = max(w, h)
        pygame.draw.rect(surf, col, (x, y, side, side), th)

    elif shape_mode == 'rhombus':
        mid_x, mid_y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        points = [(mid_x, p1[1]), (p2[0], mid_y), (mid_x, p2[1]), (p1[0], mid_y)]
        pygame.draw.polygon(surf, col, points, th)

    elif shape_mode == 'right_triangle':
        points = [p1, (p1[0], p2[1]), p2]
        pygame.draw.polygon(surf, col, points, th)

    elif shape_mode == 'equi_triangle':
        side = w
        height = (math.sqrt(3) / 2) * side
        points = [
            (p1[0], p1[1] - height / 2),
            (p1[0] - side / 2, p1[1] + height / 2),
            (p1[0] + side / 2, p1[1] + height / 2)
        ]
        pygame.draw.polygon(surf, col, points, th)


def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))
    if target_color == new_color: return

    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()
        if surface.get_at((curr_x, curr_y)) != target_color: continue

        surface.set_at((curr_x, curr_y), new_color)

        if curr_x + 1 < width: stack.append((curr_x + 1, curr_y))
        if curr_x - 1 >= 0: stack.append((curr_x - 1, curr_y))
        if curr_y + 1 < height: stack.append((curr_x, curr_y + 1))
        if curr_y - 1 >= 0: stack.append((curr_x, curr_y - 1))