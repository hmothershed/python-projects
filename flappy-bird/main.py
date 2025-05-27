import pygame, sys, random

# initialize pygame
pygame.init()

game_state = 1
score = 0
has_moved = False

window_width = 400
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()
fps = 60

# load images
player_img = pygame.image.load("images/player.png")
pipe_up_img = pygame.image.load("images/pipe_up.png")
pipe_down_img = pygame.image.load("images/pipe_down.png")
ground_img = pygame.image.load("images/ground.png")

bg_img = pygame.image.load("images/background.png")
bg_width = bg_img.get_width()   # used for scrolling background

# load sounds
slap_sound = pygame.mixer.Sound("sounds/slap.wav")
woosh_sound = pygame.mixer.Sound("sounds/woosh.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")

# load fonts
font = pygame.font.Font("fonts/flappy-font.ttf", 40)

bg_scroll_spd = 1
ground_scroll_spd = 2

# player class definition
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0   # vertical speed

    def jump(self):
        self.velocity = -10  # jump speed
        

    def update(self):
        self.velocity += 0.5  # apply gravity
        self.y += self.velocity     # update position
    
    def draw(self):
        screen.blit(player_img, (self.x, self.y))

# pipe class definition
class Pipe:
    def __init__(self, x, height, gap, velocity):
        self.x = x
        self.height = height    # height of the upper pipe
        self.gap = gap  # gap between upper and lower pipe
        self.velocity = velocity    # pipe movement speed
        self.scored = False

    def update(self):
        self.x -= self.velocity
    
    def draw(self):
        # draw upper pipe
        screen.blit(pipe_down_img, (self.x, 0 - pipe_down_img.get_height() + self.height))
        # draw lower pipe
        screen.blit(pipe_up_img, (self.x, self.height + self.gap))

# function to display the score
def scoreboard():
    show_score = font.render(str(score), True, (255, 255, 255))
    score_rect = show_score.get_rect(center=(window_width//2, 64))
    screen.blit(show_score, score_rect)

# function to show the main screen
def show_main_screen():
    title_font = pygame.font.Font("fonts/flappy-font.ttf", 60)
    small_font = pygame.font.Font("fonts/flappy-font.ttf", 30)

    title_text = title_font.render("Flappy Puff", True, (255, 255, 255))
    prompt_text = small_font.render("Press SPACE to play", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(window_width // 2, window_height // 3))
    prompt_rect = prompt_text.get_rect(center=(window_width // 2, window_height // 2))

    bg_x_pos = 0
    ground_x_pos = 0

    # loop to display the title screen until space is pressed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # exit the main screen

        # scroll background and ground
        bg_x_pos -= bg_scroll_spd
        ground_x_pos -= ground_scroll_spd
        if bg_x_pos <= -bg_width:
            bg_x_pos = 0
        if ground_x_pos <= -bg_width:
            ground_x_pos = 0

        # draw everything on the screen
        screen.blit(bg_img, (bg_x_pos, 0))
        screen.blit(bg_img, (bg_x_pos + bg_width, 0))
        screen.blit(ground_img, (ground_x_pos, 536))
        screen.blit(ground_img, (ground_x_pos + bg_width, 536))
        screen.blit(title_text, title_rect)
        screen.blit(prompt_text, prompt_rect)

        pygame.display.flip()
        clock.tick(fps)

# function to display the game over screen and handle user input to restart or quit
def game_over_screen():
    title_font = pygame.font.Font("fonts/flappy-font.ttf", 60)
    small_font = pygame.font.Font("fonts/flappy-font.ttf", 30)

    title_text = title_font.render("Game Over", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(window_width // 2, window_height // 3))

    restart_text = small_font.render("Restart?", True, (0, 0, 0))
    quit_text = small_font.render("Quit?", True, (0, 0, 0))

    restart_button = pygame.Rect(window_width // 2 - 100, window_height // 2, 200, 50)
    quit_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 70, 200, 50)

    # display gave over screen until user clicks restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return "restart"
                elif quit_button.collidepoint(event.pos):
                    return "quit"

        # draw everything for game over screen
        screen.fill((0, 0, 0))
        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, (255, 255, 255), restart_button)
        pygame.draw.rect(screen, (255, 255, 255), quit_button)
        screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        pygame.display.flip()
        clock.tick(fps)

# main game function
def game():
    global game_state, score, has_moved
    bg_x_pos = 0
    ground_x_pos = 0

    # create player and initial pipe
    player = Player(168, 300)
    pipes = [Pipe(600, random.randint(30, 250), 200, 2.4)]

    while game_state != 0:
        # gameplay
        while game_state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    has_moved = True
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(woosh_sound)
                        player.jump()

            if has_moved == True:
                player.update()

                player_rect = pygame.Rect(player.x, player.y, player_img.get_width(), player_img.get_height())

                # check for collision with pipes
                for pipe in pipes:
                    pipe_width = pipe_up_img.get_width()
                    pipe_top_height = pipe.height
                    pipe_gap = pipe.gap
                    pipe_bottom_y = pipe_top_height + pipe_gap

                    pipe_top_rect = pygame.Rect(pipe.x, 0, pipe_width, pipe_top_height)
                    pipe_bottom_rect = pygame.Rect(pipe.x, pipe_bottom_y, pipe_width, window_height - pipe_bottom_y)

                    if player_rect.colliderect(pipe_top_rect) or player_rect.colliderect(pipe_bottom_rect):
                        pygame.mixer.Sound.play(slap_sound)
                        result = game_over_screen()
                        if result == "restart":
                            return game()
                        elif result == "quit":
                            return  # close the game

                # check for collision with ground and ceiling
                if player.y < -64 or player.y > 536:
                    pygame.mixer.Sound.play(slap_sound)
                    result = game_over_screen()
                    if result == "restart":
                        return game()
                    elif result == "quit":
                        return  # close the game

                # update pipes
                for pipe in pipes:
                    pipe.update()

                # remove pipes that have gone off screen and add new ones
                if pipes[0].x < -pipe_up_img.get_width():
                    pipes.pop(0)
                    pipes.append(Pipe(400, random.randint(30, 280), 200, 2.4))

                # check for scoring
                for pipe in pipes:
                    if not pipe.scored and pipe.x + pipe_up_img.get_width() < player.x:
                        score += 1
                        pipe.scored = True
                        pygame.mixer.Sound.play(score_sound)

            
            bg_x_pos -= bg_scroll_spd
            ground_x_pos -= ground_scroll_spd
            if bg_x_pos <= -bg_width:
                bg_x_pos = 0
            if ground_x_pos <= -bg_width:
                ground_x_pos = 0

            # draw everything on the screen
            screen.blit(bg_img, (bg_x_pos, 0))
            screen.blit(bg_img, (bg_x_pos + bg_width, 0))
            screen.blit(ground_img, (ground_x_pos, 536))
            screen.blit(ground_img, (ground_x_pos + bg_width, 536))

            for pipe in pipes:
                pipe.draw()
            
            player.draw()
            scoreboard()

            pygame.display.flip()
            clock.tick(fps)

# start with main screen and then run the game
show_main_screen()
game()