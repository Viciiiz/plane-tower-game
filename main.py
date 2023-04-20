import math
import pygame
import random
from entities import Enemies, Player, EnemyBoat, EnemyPlane
from my_vars.my_vars import WINDOW_WIDTH, WINDOW_HEIGHT, window, BLACK, WHITE, PLAYER_WIDTH, PLAYER_HEIGHT, player_x, player_y, \
    player_speed, font, score, obstacle_plane_width, obstacle_plane_height, obstacle_boat_width, obstacle_boat_height, \
        obstacle_plane_x, obstacle_plane_y, obstacle_boat_x, obstacle_boat_y, game_over


pygame.display.set_caption("Avoid the Obstacles")

# set up the game clock
clock = pygame.time.Clock()


# create a group to hold all enemy sprites
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


player = Player.Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, player_speed)
player_group.add(player)


# function to create enemy sprites
def create_enemy(obstacle_width, obstacle_height, speed_range_x, speed_range_y):
    if random.randint(0,1):
        enemy = EnemyPlane.EnemyPlane(random.randint(0, WINDOW_WIDTH), 0,
                    obstacle_width, obstacle_height, speed_range_x, speed_range_y, bullet_group, shoot_delay)
    else:
        enemy = EnemyBoat.EnemyBoat(random.randint(0, WINDOW_WIDTH), 0,
                    obstacle_width, obstacle_height, speed_range_x, speed_range_y, bullet_group, shoot_delay)
    while any(pygame.sprite.spritecollide(enemy, enemy_group, False, collided=None)):
        enemy.rect.x = random.randint(0, WINDOW_WIDTH - enemy.rect.width)
        enemy.rect.y = random.randint(0, abs(int(WINDOW_HEIGHT/10) - enemy.rect.height))
    enemy_group.add(enemy)

shoot_delay = 3000
Enemies.groups = [enemy_group]
TIME_BEFORE_SPAWN = 1000
ENEMY_DISTANCE_THRESHOLD = 100
MAX_ENEMIES = 50
ENEMY_INTERVAL = 5000
enemy_timer = pygame.time.get_ticks()
num_enemies = 0
game_time = 0  # Total time elapsed since the start of the game
FPS = 60

# set a variable to store the time that the delay started
delay_start_time = pygame.time.get_ticks()


# function to display score
def display_score():
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (10, 10))
    pygame.display.update()
    
# function to display health
def display_health():
    health_text = font.render("Health: " + str(player.health), True, BLACK)
    window.blit(health_text, (400, 10))
    pygame.display.update()

# game loop
while not game_over:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
    game_time += clock.tick(FPS)
            
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
    player.move(keys)
    player.draw() 
    
       
    # draw the game
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
            
    # check how much time has passed since the delay started
    time_since_delay_start = pygame.time.get_ticks() - delay_start_time
    
    # Check if it's time to spawn a new enemy
    if pygame.time.get_ticks() - enemy_timer >= ENEMY_INTERVAL and num_enemies < MAX_ENEMIES:
        # Create a new enemy and add it to the group
        # type = ""
        # if random.randint(0, 1):
        #     type = "plane"
        create_enemy(obstacle_plane_width, obstacle_plane_height, random.randint(2, 4), random.randint(2, 4))
        # else:
        #     type = "boat"
        # create_enemy(obstacle_boat_width, obstacle_boat_height, random.randint(1, 3), random.randint(1, 3))
        num_enemies += 1
        enemy_timer = pygame.time.get_ticks()
            
    # move enemies
    for enemy in enemy_group:
        enemy.move()
        
        # make sure the enemies don't overlap if they are the same type
        for other_enemy in enemy_group:
            if enemy != other_enemy and ((enemy.getType() == "boat" and other_enemy.getType() == "boat") or \
                (enemy.getType() == "plane" and other_enemy.getType() == "plane")):
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
        if enemy.getType() == "plane" and player_x + PLAYER_WIDTH > enemy.rect.x and player_x < enemy.rect.x + enemy.rect.width \
            and player_y + PLAYER_HEIGHT > enemy.rect.y and player_y < enemy.rect.y + enemy.rect.height:
            game_over = True
            
    # handle collision between player and bullet
    for bullet in bullet_group:
        if player.rect.colliderect(bullet.rect):
            player.health -= 1
            bullet_group.remove(bullet)
            if player.health == 0:
               game_over = True
               pygame.quit() 

    
    for enemy in enemy_group:
        enemy.draw()
            
    for bullet in bullet_group:
        bullet.move()
        bullet.draw()
    
    
    display_health()
    display_score()
    
    # Increase the number of enemies over time
    # if game_time >= 10000:  # Increase after 10 seconds
    #     MAX_ENEMIES = 20
    #     ENEMY_INTERVAL = 4000
    # if game_time >= 20000:  # Increase after 20 seconds
    #     MAX_ENEMIES = 30
    #     ENEMY_INTERVAL = 3000
    
    # decrease shoot delay over time
    # if game_time >= 5000:  # Increase after 10 seconds
    #     for enemy in enemy_group:
    #         enemy.setShootDelay(shoot_delay - 500)
    #         shoot_delay -= 500


    # set the game's FPS
    clock.tick(FPS)

# quit pygame
pygame.quit()

# to do
# separate ship and planes maybe?
# make the player's plane fly over the boats: different depths