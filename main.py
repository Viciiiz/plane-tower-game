import pygame
import random
from entities import Enemies
from my_vars.my_vars import WINDOW_WIDTH, WINDOW_HEIGHT, window, BLACK, WHITE, PLAYER_WIDTH, PLAYER_HEIGHT, player_x, player_y, \
    player_speed, font, score, obstacle_width, obstacle_height, obstacle_x, obstacle_y, game_over


pygame.display.set_caption("Avoid the Obstacles")

# set up the game clock
clock = pygame.time.Clock()


if random.randint(0, 1):
    obstacle_speed_x = random.choice([-3, 3])
else:
    obstacle_speed_x = 0
obstacle_speed_y = 3
obstacle = Enemies.Enemies(obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_speed_x, obstacle_speed_y)

# game loop
# game_over = False
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
