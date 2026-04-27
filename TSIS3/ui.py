import pygame

def draw_text(screen, text, size, x, y, color=(0, 0, 0), center=False):
    font = pygame.font.SysFont("Verdana", size)
    img = font.render(text, True, color)
    rect = img.get_rect(topleft=(x, y))
    if center:
        rect.center = (x, y)
    screen.blit(img, rect)

class Button:
    def __init__(self, x, y, w, h, text, color=(200, 200, 200), hover_color=(170, 170, 170)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=5)
        draw_text(screen, self.text, 20, self.rect.centerx, self.rect.centery, center=True)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False