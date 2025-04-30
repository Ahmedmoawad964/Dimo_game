import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game - Fast & Restartable")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
RED = (200, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (160, 82, 45)
CLOUD_WHITE = (240, 240, 240)

# Dino class
class Dino:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.width = 40
        self.height = 60
        self.is_jumping = False
        self.jump_speed = 15
        self.gravity = 1
        self.velocity = 0

    def jump(self):
        if not self.is_jumping:
            self.velocity = -self.jump_speed
            self.is_jumping = True

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y >= 300:
            self.y = 300
            self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Cactus class
class Cactus:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = 340
        self.width = 20
        self.height = 40
        self.speed = 7

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Cloud class
class Cloud:
    def __init__(self):
        self.x = random.randint(600, 1000)
        self.y = random.randint(50, 150)
        self.width = 60
        self.height = 30
        self.speed = 2

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, CLOUD_WHITE, (self.x, self.y, self.width, self.height))

# Function to detect collision
def detect_collision(dino, cactus):
    dino_rect = pygame.Rect(dino.x, dino.y, dino.width, dino.height)
    cactus_rect = pygame.Rect(cactus.x, cactus.y, cactus.width, cactus.height)
    return dino_rect.colliderect(cactus_rect)

# Game function
def game():
    clock = pygame.time.Clock()
    dino = Dino()
    cactuses = [Cactus()]
    clouds = [Cloud() for _ in range(2)]
    score = 0
    font = pygame.font.SysFont(None, 40)
    running = True

    while running:
        clock.tick(60)  # زودنا الفريمات لـ 60 FPS عشان السلاسة
        screen.fill(SKY_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        # Draw clouds
        for cloud in list(clouds):
            cloud.update()
            cloud.draw(screen)
            if cloud.x < -cloud.width:
                clouds.remove(cloud)

        if random.randint(1, 200) == 1:
            clouds.append(Cloud())

        pygame.draw.rect(screen, GROUND_BROWN, (0, 360, SCREEN_WIDTH, 40))

        dino.update()
        dino.draw(screen)

        for cactus in list(cactuses):
            cactus.update()
            cactus.draw(screen)

            if cactus.x < -cactus.width:
                cactuses.remove(cactus)
                score += 10

            if detect_collision(dino, cactus):
                game_over()

        if len(cactuses) == 0 or cactuses[-1].x < 400:
            cactuses.append(Cactus())

        for cactus in cactuses:
            cactus.speed = 7 + (score // 50)  # سرعة أعلى

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if score >= 600:
            win_screen()

        pygame.display.update()

# Game Over screen
def game_over():
    font = pygame.font.SysFont(None, 60)
    over_text = font.render("Game Over! Press R to Restart", True, RED)
    screen.blit(over_text, (SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 30))
    pygame.display.update()
    wait_for_restart()

# Win screen
def win_screen():
    font = pygame.font.SysFont(None, 60)
    win_text = font.render("You Win! Press R to Restart", True, GREEN)
    screen.blit(win_text, (SCREEN_WIDTH//2 - 230, SCREEN_HEIGHT//2 - 30))
    pygame.display.update()
    wait_for_restart()

# Wait for Restart
def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game()

# Main
if __name__ == "__main__":
    game()