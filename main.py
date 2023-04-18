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
# obstacle = Enemies.Enemies(obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_speed_x, obstacle_speed_y)



# create a group to hold all enemy sprites
enemy_group = pygame.sprite.Group()

# create five enemy sprites and add them to the group
for i in range(5):
    enemy = Enemies.Enemies(obstacle_x, obstacle_y, obstacle_width, obstacle_height, obstacle_speed_x, obstacle_speed_y)
    enemy_group.add(enemy)



# game loop
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
    if keys[pygame.K_DOWN] and player_y < WINDOW_HEIGHT - PLAYER_WIDTH:
        player_y += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed

    # handle obstacle movement
    # obstacle.move()
    # if obstacle.y > WINDOW_HEIGHT or obstacle.x > WINDOW_WIDTH or obstacle.x < 0:
    #     obstacle.reset()
    #     score += 1
    # enemy_group.move()
    # move each enemy sprite in the group
    for enemy in enemy_group:
        enemy.move()

    for enemy in enemy_group:
        if enemy.rect.y > WINDOW_HEIGHT or enemy.rect.x > WINDOW_WIDTH or enemy.rect.x < 0:
            enemy.reset()
            score += 1

    # handle collision detection
    for enemy in enemy_group:
        if player_x + PLAYER_WIDTH > enemy.rect.x and player_x < enemy.rect.x + enemy.width \
            and player_y + PLAYER_HEIGHT > enemy.rect.y and player_y < enemy.rect.y + enemy.height:
            game_over = True

    # draw the game
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
    
    for enemy in enemy_group:
        enemy.draw()
    
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (10, 10))
    pygame.display.update()


    # set the game's FPS
    clock.tick(60)

# quit pygame
pygame.quit()
