import pygame
import random

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bounce Simulation")

# Load and scale background
try:
    background = pygame.image.load('background.jpg')
except pygame.error as e:
    print(f"Unable to load image: {e}")
    background = None

if background:
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load and scale ball image once
ball_img = pygame.image.load('ball.png')
ball_img = pygame.transform.scale(ball_img, (50, 50))  # Smaller size for better visuals

# Load pixel font
font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
title_text = font.render("Bounce Simulation", True, (255, 255, 255))


# Button rendering function
def draw_button(rect, text, bg_color):
    pygame.draw.rect(screen, bg_color, rect, border_radius=12)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# Define buttons
start_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 50)
restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)

# Ball class
class Ball:
    GRAVITY = 0.5

    def __init__(self):
        self.image = ball_img
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(0, HEIGHT // 2)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)

    def move(self):
        self.vy += self.GRAVITY
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - 50:
            self.vx *= -1

        # Bounce off floor and ceiling
        if self.y <= 0:
            self.vy *= -1
            self.y = 0
        elif self.y >= HEIGHT - 50:
            self.vy *= -0.9  # simulate energy loss
            self.y = HEIGHT - 50
            if abs(self.vy) < 1:
                self.vy = 0  # stop small bounces

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def is_stopped(self):
        return self.vy == 0 and self.y >= HEIGHT - 50

# Game state
balls = []
simulation_started = False
simulation_over = False

clock = pygame.time.Clock()
running = True

# Main loop
while running:
    screen.blit(background, (0, 0)) if background else screen.fill((30, 30, 30))

    # Draw title
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not simulation_started and start_btn.collidepoint(event.pos):
                balls = [Ball() for _ in range(5)]
                simulation_started = True
                simulation_over = False
            elif simulation_over and restart_btn.collidepoint(event.pos):
                balls = [Ball() for _ in range(5)]
                simulation_started = True
                simulation_over = False

    # Simulation logic
    if simulation_started:
        all_stopped = True
        for ball in balls:
            ball.move()
            ball.render(screen)
            if not ball.is_stopped():
                all_stopped = False
        if all_stopped:
            simulation_over = True
            simulation_started = False

    # UI logic
    if not simulation_started and not simulation_over:
        draw_button(start_btn, "START", (0, 200, 0))

    if simulation_over:
        draw_button(restart_btn, "RESTART?", (255, 165, 0))  # Orange

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
