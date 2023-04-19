import math
import pygame
import random
from entities import Enemies
from my_vars.my_vars import WINDOW_WIDTH, WINDOW_HEIGHT, window, BLACK, WHITE, PLAYER_WIDTH, PLAYER_HEIGHT, player_x, player_y, \
    player_speed, font, score, obstacle_plane_width, obstacle_plane_height, obstacle_boat_width, obstacle_boat_height, \
        obstacle_plane_x, obstacle_plane_y, obstacle_boat_x, obstacle_boat_y, game_over


pygame.display.set_caption("Avoid the Obstacles")

# set up the game clock
clock = pygame.time.Clock()


if random.randint(0, 1):
    obstacle_speed_x = random.choice([-3, 3])
else:
    obstacle_speed_x = 0
obstacle_speed_y = 3


# create a group to hold all enemy sprites
enemy_group = pygame.sprite.Group()


def create_enemy(obstacle_width, obstacle_height, speed_range_x, speed_range_y, type):
    enemy = Enemies.Enemies(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT/2),
                    obstacle_width, obstacle_height, speed_range_x, speed_range_y, type)
    while any(pygame.sprite.spritecollide(enemy, enemy_group, False, collided=None)):
        enemy.rect.x = random.randint(0, WINDOW_WIDTH - enemy.rect.width)
        enemy.rect.y = random.randint(0, WINDOW_HEIGHT - enemy.rect.height)
    enemy_group.add(enemy)

# create five enemy sprites and add them to the group
for i in range(5):
    type = ""
    if random.randint(0, 1):
        type = "plane"
        create_enemy(obstacle_plane_width, obstacle_plane_height, random.randint(2, 4), random.randint(2, 4), "plane")
    else:
        type = "boat"
        create_enemy(obstacle_boat_width, obstacle_boat_height, random.randint(1, 3), random.randint(1, 3), "boat")


Enemies.groups = [enemy_group]

ENEMY_DISTANCE_THRESHOLD = 100


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

    # move enemies
    for enemy in enemy_group:
        enemy.move()
        
        # make sure the enemies don't overlap
        for other_enemy in enemy_group:
            if enemy != other_enemy:
                dx = enemy.rect.x - other_enemy.rect.x
                dy = enemy.rect.y - other_enemy.rect.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < ENEMY_DISTANCE_THRESHOLD:
                    # if two enemies are too close, move one of them away
                    angle = math.atan2(dy, dx)
                    enemy.rect.x += math.cos(angle) * (ENEMY_DISTANCE_THRESHOLD - distance) / 2
                    enemy.rect.y += math.sin(angle) * (ENEMY_DISTANCE_THRESHOLD - distance) / 2
                    break
                

    # reset position of enemy objects and update score 
    for enemy in enemy_group:
        if enemy.rect.y > WINDOW_HEIGHT or enemy.rect.x > WINDOW_WIDTH or enemy.rect.x < 0:
            enemy.reset()
            score += 1

    # handle collision detection between enemies and player
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
