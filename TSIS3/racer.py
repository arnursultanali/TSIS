import pygame
import random

WIDTH, HEIGHT = 400, 600

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name="red"):
        super().__init__()
        img = pygame.image.load("player.png")
        self.image = pygame.transform.scale(img, (50, 90))
        self.rect = self.image.get_rect(center=(160, 520))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        img = pygame.image.load("enemy.png")
        self.image = pygame.transform.scale(img, (50, 90))
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -100))
        self.speed = speed

    def update(self, current_speed):
        self.rect.y += current_speed
        if self.rect.top > HEIGHT:
            self.rect.top = -100
            self.rect.centerx = random.randint(40, WIDTH-40)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.image.load("coin.png").convert_alpha()
        self.spawn()

    def spawn(self):
        self.weight = random.choice([1, 1, 1, 3]) # 25% chance for weight 3
        size = 35 if self.weight == 1 else 50
        self.image = pygame.transform.scale(self.image_orig, (size, size))
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))
        self.image.set_colorkey((255, 255, 255))

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.spawn()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type # 'nitro', 'shield', 'repair'
        self.image = pygame.Surface((30, 30))
        colors = {'nitro': (255, 255, 0), 'shield': (0, 255, 255), 'repair': (0, 255, 0)}
        self.image.fill(colors[p_type])
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.kill()

class Hazard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((139, 69, 19)) # Brown for oil/pothole
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -50))

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.kill()