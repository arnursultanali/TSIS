import pygame
import sys
import json
import os
from db import Database
from game import Snake, Food
from config import DB_CONFIG, SCREEN_WIDTH, SCREEN_HEIGHT

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake TSIS4 - PostgreSQL Edition')
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 20)

# Подключение к БД
db = Database(DB_CONFIG)

def load_settings():
    """Безопасная загрузка настроек с защитой от KeyError."""
    default_settings = {
        "snake_color": [0, 255, 0], 
        "grid": True, 
        "sound": True,
        "speed": 10
    }
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                user_data = json.load(f)
                return {**default_settings, **user_data}
        return default_settings
    except (FileNotFoundError, json.JSONDecodeError):
        return default_settings

def main():
    # 1. Загрузка настроек и ввод имени
    settings = load_settings()
    username = input("Enter Username: ").strip()
    if not username:
        username = "Guest"

    # 2. Синхронизация с БД (Загрузка прогресса)
    user_info = db.get_user(username)
    if not user_info:
        db.create_user(username)
        score = 0
        level = 1
    else:
        score, level = user_info

    # Инициализация объектов
    snake = Snake(settings['snake_color'])
    food = Food((255, 0, 0), 1) # Указываем цвет и вес еды
    food.spawn([], snake.body)

    running = True
    while running:
        screen.fill((0, 0, 0)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Сохраняем результат при закрытии окна
                db.update_user_progress(username, score, level)
                pygame.quit()
                sys.exit()

            # Управление змейкой
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 20):
                    snake.direction = (0, -20)
                if event.key == pygame.K_DOWN and snake.direction != (0, -20):
                    snake.direction = (0, 20)
                if event.key == pygame.K_LEFT and snake.direction != (20, 0):
                    snake.direction = (-20, 0)
                if event.key == pygame.K_RIGHT and snake.direction != (-20, 0):
                    snake.direction = (20, 0)

        # Движение змейки
        head = snake.move()

        # Проверка столкновений
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or
                head[1] < 0 or head[1] >= SCREEN_HEIGHT or
                head in snake.body[1:]):
            print(f"Game Over! Final Score: {score}")
            db.update_user_progress(username, score, level) # Сохранение
            running = False

        # Поедание еды
        if head == food.pos:
            score += food.weight
            food.spawn([], snake.body)
            if score % 3 == 0:
                level += 1
        else:
            # Если не съели еду, удаляем хвост (движение)
            if len(snake.body) > 1:
                snake.body.pop()

        # ОТРИСОВКА
        for block in snake.body:
            pygame.draw.rect(screen, snake.color, (block[0], block[1], 18, 18))

        pygame.draw.rect(screen, (255, 0, 0), (food.pos[0], food.pos[1], 20, 20))

        # Текст
        info_txt = font_small.render(f"User: {username} | Score: {score} | Level: {level}", True, (255, 255, 255))
        screen.blit(info_txt, (10, 10))

        pygame.display.flip()
        clock.tick(settings['speed'] + level)

    pygame.quit()

if __name__ == "__main__":
    main()