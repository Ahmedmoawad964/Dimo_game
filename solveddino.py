import pygame
import random
import sys

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino AI Game with A*")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (50, 50, 50)
OBSTACLE_COLOR = (200, 50, 50)
DINO_COLOR = (50, 200, 50)
WIN_BACKGROUND_COLOR = (173, 216, 230)

# Clock and frame rate
clock = pygame.time.Clock()
FPS = 60

# Dino (player) settings
dino_width, dino_height = 30, 40
dino_x = 100
dino_y = HEIGHT - dino_height - 40
dino_vel_y = 0
gravity = 1
jump_force = -15
is_jumping = False

# Obstacle class
class Obstacle:
    def __init__(self, speed):
        self.x = WIDTH
        self.y = HEIGHT - random.randint(30, 60)
        self.width = random.randint(20, 50)
        self.height = random.randint(30, 40)
        self.speed = speed

    def move(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, pygame.Rect(self.x, self.y, self.width, self.height))

# Score and difficulty settings
score = 0
target_score = 1000
base_speed = 6
difficulty_increase_interval = 300  # Speed increases every 300 points

# Fonts
font = pygame.font.SysFont(None, 40)
win_font = pygame.font.SysFont(None, 60)

# AI Decision function using A* 
def ai_should_jump_astar(dino_x, dino_y, obstacles):
    for obs in obstacles:
        distance = obs.x - dino_x
        if distance > 0:
            g = distance  # Cost from start to obstacle
            h = obs.speed * 10  # Heuristic estimation
            f = g + h
            if f < 200 and dino_y >= HEIGHT - dino_height - 40:
                return True
    return False

# Drawing function for game window
def draw_window():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 40, WIDTH, 40))
    pygame.draw.rect(screen, DINO_COLOR, (dino_x, dino_y, dino_width, dino_height))
    for obs in obstacles:
        obs.draw()
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.update()

# Display the winning screen
def show_win_screen():
    screen.fill(WIN_BACKGROUND_COLOR)
    win_text = win_font.render("🎉 Congratulations! You Win! 🎉", True, BLACK)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()
    pygame.time.delay(3000)

# Main Game Loop
obstacles = []
obstacle_timer = 0
run = True

while run:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Increase obstacle speed based on score
    current_speed = base_speed + (score // difficulty_increase_interval)

    # AI decision: should the dino jump?
    if ai_should_jump_astar(dino_x, dino_y, obstacles):
        if not is_jumping:
            dino_vel_y = jump_force
            is_jumping = True

    # Apply physics
    dino_y += dino_vel_y
    dino_vel_y += gravity
    if dino_y >= HEIGHT - dino_height - 40:
        dino_y = HEIGHT - dino_height - 40
        is_jumping = False

    # Spawn new obstacles
    obstacle_timer += 1
    if obstacle_timer > 70:
        obstacles.append(Obstacle(current_speed))
        obstacle_timer = 0

    # Move obstacles
    for obs in obstacles:
        obs.move()

    # Remove obstacles that go off-screen
    obstacles = [obs for obs in obstacles if obs.x > -obs.width]

    # Collision detection
    for obs in obstacles:
        if pygame.Rect(dino_x, dino_y, dino_width, dino_height).colliderect(pygame.Rect(obs.x, obs.y, obs.width, obs.height)):
            print("Game Over! Dino Crashed!")
            pygame.quit()
            sys.exit()

    # Update score
    score += 1
    if score >= target_score:
        print("🎉 Congratulations! AI Won the Game!")
        show_win_screen()
        pygame.quit()
        sys.exit()

    # Draw everything
    draw_window()