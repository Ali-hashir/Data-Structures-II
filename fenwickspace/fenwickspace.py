import pygame
import random

# Define some constants
WIDTH = 640
HEIGHT = 480
FPS = 60
ENEMY_SPEED = 4.5     
BULLET_SPEED = 10.5
pygame.font.init()
SCORE_FONT = pygame.font.SysFont("Times New Roman", 20) 

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
 
    def update(self, idx, val):
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & -idx
 
    def query(self, idx):
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image = pygame.image.load("spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(player_image, (45, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.score = FenwickTree(WIDTH)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(enemy_image, (65, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)

    def update(self):
        self.rect.y += ENEMY_SPEED
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        bullet_image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.scale(bullet_image, (25, 40)) 
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FenwickSpace")
clock = pygame.time.Clock()

# Load the background image
bg = pygame.image.load("spacebg.jpg").convert()

#create the player sprite and sprite groups
player = Player()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)

#creating enemy spaceships
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Set a threshold for the number of enemies on the screen
ENEMY_THRESHOLD = 8

# Welcome screen
welcome_screen = True
while welcome_screen:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            welcome_screen = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the start button was clicked
            if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                welcome_screen = False

    # Draw a colorful image
    image = pygame.image.load("spacebg.jpg")
    image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2)) 
    screen.blit(image, image_rect)

    # Draw the start button
    start_button_rect = pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2 - 49.5, HEIGHT // 2 + 104.5, 100, 50))
    start_text = pygame.font.Font("Machine BT.ttf", 22).render("Start Game", True, (255, 0, 0))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 115))

    # Draw the welcome screen
    title_text = pygame.font.Font("Machine BT.ttf", 55).render("FENWICKSPACE", True, (0, 0, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4.8))

    welcome_text = pygame.font.Font("Machine BT.ttf", 32).render("A Mini Project By Maaz, Ahsan, Zain and Ali", True, (0, 0, 255))
    screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, HEIGHT // 2.5))

    desc_text = pygame.font.Font("Machine BT.ttf", 18).render("(A simple 2D shooting game made using a Fenwick Tree to keep track of the score)", True, (0, 0, 255))
    screen.blit(desc_text, (WIDTH // 2 - desc_text.get_width() // 2, HEIGHT // 2))


    pygame.display.flip()


# Main game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update the game state
    all_sprites.update()

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for enemy in hits:
        player.score.update(enemy.rect.centerx, 10)

    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # Add new enemies if the number on screen is below the threshold
    if len(enemies) < ENEMY_THRESHOLD:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw the game state
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    score_text = SCORE_FONT.render(f"Points: {player.score.query(HEIGHT)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

# Game over screen
game_over = True
while game_over:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False

    # Draw the game over screen
    screen.fill((255, 182, 193))
    game_over_text = SCORE_FONT.render("Game Over !", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
    final_score_text = SCORE_FONT.render(f"Final Score: {player.score.query(WIDTH)}", True, (255, 0, 0))
    screen.blit(final_score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
    pygame.display.flip()


pygame.quit()

