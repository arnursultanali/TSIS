import pygame, sys, time, random, os
from racer import Player, Enemy, Coin, PowerUp, Hazard
from ui import Button, draw_text
from persistence import load_data, save_data, update_leaderboard

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Arcade")
clock = pygame.time.Clock()


settings = load_data('settings.json', {"sound": True, "car_color": "red", "difficulty": 1})

try:
    bg = pygame.transform.scale(pygame.image.load("road.jpg"), (WIDTH, HEIGHT))
except pygame.error:
 
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((100, 100, 100))

def game_loop():
    speed = 5 + settings['difficulty']
    score, coins_count = 0, 0
    lives = 1
    N = 5
    active_buff = None
    buff_timer = 0
    shielded = False

    player = Player(settings['car_color'])
    enemies = pygame.sprite.Group(Enemy(speed))
    coins = pygame.sprite.Group(Coin())
    powerups = pygame.sprite.Group()
    hazards = pygame.sprite.Group()

    bg_y = 0
    running = True
    while running:
        
        current_speed = speed * 1.5 if active_buff == 'nitro' else speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - HEIGHT))
        bg_y = (bg_y + current_speed) % HEIGHT

      
        player.move()
        enemies.update(current_speed)
        coins.update(current_speed)
        powerups.update(current_speed)
        hazards.update(current_speed)

   
        if random.random() < 0.01: hazards.add(Hazard())
        if random.random() < 0.005: powerups.add(PowerUp(random.choice(['nitro', 'shield', 'repair'])))

        
        coin_hit = pygame.sprite.spritecollideany(player, coins)
        if coin_hit:
            coins_count += coin_hit.weight
            if coins_count // N > (coins_count - coin_hit.weight) // N:
                speed += 0.5
            coin_hit.spawn()


        p_hit = pygame.sprite.spritecollideany(player, powerups)
        if p_hit:
            if p_hit.type == 'nitro':
                active_buff = 'nitro'
                buff_timer = time.time() + 4
            elif p_hit.type == 'shield':
                shielded = True
            elif p_hit.type == 'repair':
                lives += 1  # Логика Repair: добавляем жизнь
            p_hit.kill()

   
        if active_buff == 'nitro' and time.time() > buff_timer:
            active_buff = None

       
        enemy_hit = pygame.sprite.spritecollideany(player, enemies)
        hazard_hit = pygame.sprite.spritecollideany(player, hazards)

        if enemy_hit or hazard_hit:
            if shielded:
                shielded = False
                if hazard_hit: hazard_hit.kill()
                if enemy_hit: enemy_hit.rect.top = -100
            else:
                lives -= 1  
                if hazard_hit: hazard_hit.kill()
                if enemy_hit: enemy_hit.rect.top = -100
                
                if lives <= 0:
                    update_leaderboard("Player", coins_count)
                    return "GAME_OVER", coins_count

  
        enemies.draw(screen)
        coins.draw(screen)
        powerups.draw(screen)
        hazards.draw(screen)
        screen.blit(player.image, player.rect)


        draw_text(screen, f"Coins: {coins_count}", 20, 10, 10, (0, 0, 0))
        draw_text(screen, f"HP: {lives}", 20, 10, 40, (200, 0, 0))
        if shielded: draw_text(screen, "SHIELD ON", 15, 10, 70, (0, 200, 200))
        if active_buff == 'nitro': draw_text(screen, "NITRO BOOST", 15, 10, 90, (255, 100, 0))

        pygame.display.update()
        clock.tick(60)

def main_menu():
    btn_play = Button(100, 200, 200, 50, "PLAY")
    btn_lb = Button(100, 270, 200, 50, "LEADERBOARD")
    while True:
        screen.fill((255, 255, 255))
        draw_text(screen, "RACER ARCADE", 40, WIDTH // 2, 100, center=True)
        btn_play.draw(screen)
        btn_lb.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_play.is_clicked(event): 
                game_loop()
            if btn_lb.is_clicked(event): 
                leaderboard_screen()
                
        pygame.display.update()

def leaderboard_screen():
    btn_back = Button(100, 500, 200, 50, "BACK")
    while True:
        screen.fill((240, 240, 240))
        draw_text(screen, "TOP 10", 30, WIDTH // 2, 50, center=True)
        lb = load_data('leaderboard.json', [])
        lb = sorted(lb, key=lambda x: x['score'], reverse=True)
        
        for i, entry in enumerate(lb[:10]):
            draw_text(screen, f"{i + 1}. {entry['name']} - {entry['score']}", 18, 100, 120 + i * 30)

        btn_back.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event): 
                return
        pygame.display.update()

if __name__ == "__main__":
    main_menu()