import pygame
import random
from Enemies import Enemies
import sys
 
# adding entities/ to the system path
sys.path.insert(0, 'entities/')


# initialize pygame
pygame.init()

# set up the game window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Avoid the Obstacles")

# set up the game clock
clock = pygame.time.Clock()

# set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set up the player and the player's movement speed
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
player_x = (WINDOW_WIDTH - PLAYER_WIDTH) // 2
player_y = WINDOW_HEIGHT - PLAYER_HEIGHT - 10
player_speed = 5

# set up the font for displaying the score
font = pygame.font.SysFont(None, 30)

# set up the score
score = 0




# set up the obstacle and the obstacle's movement speed
obstacle_width = 50
obstacle_height = 50
obstacle_x = random.randint(0, WINDOW_WIDTH - obstacle_width)
obstacle_y = -obstacle_height
if random.randint(0, 1):
    obstacle_speed_x = random.choice([-3, 3])
else:
    obstacle_speed_x = 0
obstacle_speed_y = 3
obstacle = Enemies(obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_speed_x, obstacle_speed_y)

# game loop
game_over = False
while not game_over:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - PLAYER_WIDTH:
        player_x += player_speed

    # handle obstacle movement
    obstacle.move()
    if obstacle.y > WINDOW_HEIGHT:
        obstacle.reset()
        score += 1

    # handle collision detection
    if player_x + PLAYER_WIDTH > obstacle.x and player_x < obstacle.x + obstacle.width and player_y + PLAYER_HEIGHT > obstacle.y and player_y < obstacle.y + obstacle.height:
        game_over = True

    # draw the game
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
    obstacle.draw()
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (10, 10))
    pygame.display.update()


    # set the game's FPS
    clock.tick(60)

# quit pygame
pygame.quit()
