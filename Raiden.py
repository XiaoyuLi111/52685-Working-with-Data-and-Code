import pygame
from pygame.constants import K_r, K_q

import random

# Initialize pygame
pygame.init()

# set constant
WIDTH = 480
HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raiden")

# Load image resources
player_img_raw = pygame.image.load('player.png')
enemy_img_raw = pygame.image.load('enemy.png')
bullet_img_raw = pygame.image.load('bullet.png')

# Resize image
player_img = pygame.transform.scale(player_img_raw, (50, 50))
enemy_img = pygame.transform.scale(enemy_img_raw, (50, 30))
bullet_img = pygame.transform.scale(bullet_img_raw, (5, 10))

# Player and enemy positions and bullets
player_pos = [WIDTH / 2, HEIGHT - 50]
enemies = []
bullets = []
enemy_bullets = []

# player health
lives = 3

# game variables
score = 0
enemy_frequency = 0.02  # Default enemy frequency

# Show start screen
def show_start_screen():
    global lives, enemy_frequency

    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    text = font.render("Choose game difficulty: ", True, BLACK)
    screen.blit(text, (WIDTH // 4, HEIGHT // 4))
    
    difficulties = ["Easy", "Medium", "Hard"]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        lives = 3
                        enemy_frequency = 0.01
                    elif selected == 1:
                        lives = 2
                        enemy_frequency = 0.02
                    else:
                        lives = 1
                        enemy_frequency = 0.05
                    return
        # Draw difficulty options
        for index, difficulty in enumerate(difficulties):
            color = RED if index == selected else BLACK
            text = font.render(difficulty, True, color)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2 + index * 40))
        
        pygame.display.flip()

# Show end screen
def show_end_screen():
    global score
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Your Score: {score}", True, BLACK)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    
    retry_text = font.render("Press 'r' to retry or 'q' to quit", True, BLACK)
    screen.blit(retry_text, (WIDTH // 6, HEIGHT // 2 + 40))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    return True
                if event.key == K_q:
                    return False


if __name__ == "__main__":
    restart = True
    while restart:
        score = 0  # Reset score
        enemies.clear()
        bullets.clear()
        enemy_bullets.clear()
        player_pos = [WIDTH / 2, HEIGHT - 50]
        
        show_start_screen()
        
        running = True
        while running:
            screen.fill(WHITE)
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_pos[0] -= 5
            if keys[pygame.K_RIGHT]:
                player_pos[0] += 5
            if keys[pygame.K_SPACE]:
                bullets.append([player_pos[0] + 22, player_pos[1]])

            # enemy aircraft
            if random.random() < 0.02:
                enemies.append([random.randint(0, WIDTH-50), 0])
                if random.random() < 0.5:  # 50% chance of shooting
                    enemy_bullets.append([enemies[-1][0] + 22, enemies[-1][1]])

            # Move enemy aircraft
            for enemy in enemies:
                enemy[1] += 2
                if enemy[1] > HEIGHT:
                    enemies.remove(enemy)

            # Move player's bullets
            for bullet in bullets:
                bullet[1] -= 5
                if bullet[1] < 0:
                    bullets.remove(bullet)

            # Move enemy bullets
            for bullet in enemy_bullets:
                bullet[1] += 5
                if bullet[1] > HEIGHT:
                    enemy_bullets.remove(bullet)

            # Check if the player's bullet hit an enemy aircraft
            bullets_to_remove = []
            enemies_to_remove = []

            for bullet in bullets:
                for enemy in enemies:
                    if (bullet[0] < enemy[0] + 50 and bullet[0] + 5 > enemy[0] and
                        bullet[1] < enemy[1] + 30 and bullet[1] + 10 > enemy[1]):
                        bullets_to_remove.append(bullet)
                        enemies_to_remove.append(enemy)

            # Remove bullets and enemy aircraft that have been hit
            for bullet in bullets_to_remove:
                if bullet in bullets:
                    bullets.remove(bullet)
                    score += 1

            for enemy in enemies_to_remove:
                if enemy in enemies:
                    enemies.remove(enemy)


            # Check if the player was hit by a bullet
            for bullet in enemy_bullets:
                if (player_pos[0] < bullet[0] + 5 and player_pos[0] + 50 > bullet[0] and
                    player_pos[1] < bullet[1] + 10 and player_pos[1] + 30 > bullet[1]):
                    enemy_bullets.remove(bullet)
                    lives -= 1

            # Check if an enemy collides with the player's aircraft
            for enemy in enemies:
                if (player_pos[0] < enemy[0] + 50 and player_pos[0] + 50 > enemy[0] and
                    player_pos[1] < enemy[1] + 30 and player_pos[1] + 30 > enemy[1]):
                    lives = 0

            # Draw players, enemies and bullets
            screen.blit(player_img, player_pos)
            for enemy in enemies:
                screen.blit(enemy_img, enemy)
            for bullet in bullets:
                screen.blit(bullet_img, bullet)
            for bullet in enemy_bullets:
                screen.blit(bullet_img, bullet)

            # draw health
            font = pygame.font.SysFont(None, 36)
            life_text = font.render(f'Lives: {lives}', True, BLACK)
            screen.blit(life_text, (10, 10))

            # draw score
            score_text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(score_text, (WIDTH - 150, 10))

            # Game over judgment
            if lives <= 0:
                running = False

            pygame.display.flip()
            pygame.time.Clock().tick(30)
        
        restart = show_end_screen()  # Determine whether to restart the game based on the return value of this function

    pygame.quit()
    exit()