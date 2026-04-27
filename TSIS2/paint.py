import pygame
import datetime
from tools import draw_shape, flood_fill

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Layers
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))

pygame.display.set_caption("Ultimate Paint - Practice 12")
clock = pygame.time.Clock()


mode = 'pencil'
color = (0, 0, 0)
thickness = 2  # Starting size: Small
start_pos = None
prev_pos = None

# Text
text_font = pygame.font.SysFont("Arial", 24)
text_content = ""
typing = False
text_pos = (0, 0)

run = True
while run:
    screen.blit(base_layer, (0, 0))
    m_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            #brush size
            if event.key == pygame.K_1: thickness = 2  # Small
            if event.key == pygame.K_2: thickness = 5  # Medium
            if event.key == pygame.K_3: thickness = 10  # Large

            #Save(Ctrl+S)
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                name = datetime.datetime.now().strftime("assets/draw_%Y%m%d_%H%M%S.png")
                pygame.image.save(base_layer, name)
                print(f"Saved: {name}")

            #Switching modes
            if event.key == pygame.K_p: mode = 'pencil'
            if event.key == pygame.K_l: mode = 'line'
            if event.key == pygame.K_r: mode = 'rectangle'
            if event.key == pygame.K_s: mode = 'square'
            if event.key == pygame.K_h: mode = 'rhombus'
            if event.key == pygame.K_t: mode = 'right_triangle'
            if event.key == pygame.K_f: mode = 'fill'
            if event.key == pygame.K_x: mode = 'text'  # Нажми X для текста
            if event.key == pygame.K_e: color = (255, 255, 255); mode = 'pencil'  # Ластик

            # Typing text
            if typing:
                if event.key == pygame.K_RETURN:
                    rendered = text_font.render(text_content, True, color)
                    base_layer.blit(rendered, text_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 'fill':
                flood_fill(base_layer, *event.pos, color)
            elif mode == 'text':
                typing = True
                text_pos = event.pos
                text_content = ""
            else:
                start_pos = event.pos
                prev_pos = event.pos  # For pencil

        if event.type == pygame.MOUSEMOTION:
            if start_pos and mode == 'pencil':
                #Pencil Tool (Freehand)
                pygame.draw.line(base_layer, color, prev_pos, m_pos, thickness)
                prev_pos = m_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if start_pos and mode not in ['pencil', 'fill', 'text']:
                draw_shape(base_layer, mode, start_pos, event.pos, color, thickness)
            start_pos = None

    # Show PREVIEW of figures (to see the process)
    if start_pos and mode not in ['pencil', 'fill', 'text']:
        draw_shape(screen, mode, start_pos, m_pos, color, thickness)

    # Display PREVIEW text
    if typing:
        t_surf = text_font.render(text_content + "|", True, color)
        screen.blit(t_surf, text_pos)

    # Toolbar
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, 40))
    ui_text = f"Mode: {mode} | Size: {thickness} | P:Pencil, L:Line, R:Rect, S:Square, H:Rhomb, F:Fill, X:Text"
    screen.blit(pygame.font.SysFont("Arial", 16).render(ui_text, True, (0, 0, 0)), (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()