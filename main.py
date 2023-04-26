import math
import pygame
import random
from entities import Enemies, Player, EnemyBoat, EnemyPlane
import json
# from game.level import levels
from my_vars.my_vars import WINDOW_WIDTH, WINDOW_HEIGHT, window, BLACK, WHITE, PLAYER_WIDTH, PLAYER_HEIGHT, player_x, player_y, \
    player_speed, font, score, obstacle_plane_width, obstacle_plane_height, obstacle_boat_width, obstacle_boat_height, \
        obstacle_plane_x, obstacle_plane_y, obstacle_boat_x, obstacle_boat_y, game_over


pygame.display.set_caption("Avoid the Obstacles")

# set up the game clock
clock = pygame.time.Clock()


# Parse the level.json data into a Python object
f = open('./game/level.json', 'r')
json_data = f.read()
f.close()
levels = json.loads(json_data)


# create a group to hold all enemy sprites
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# enemy_plane_group = pygame.sprite.LayeredUpdates()
# enemy_boat_group = pygame.sprite.LayeredUpdates() 
all_sprite_group = pygame.sprite.LayeredUpdates()


player = Player.Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, player_speed)
player_group.add(player)
all_sprite_group.add(player)


# function to create enemy sprites
def create_enemy(obstacle_width, obstacle_height, speed_range_x_boat, speed_range_y_boat, speed_range_x_plane, speed_range_y_plane, type):
    shoot_delay = 2500 + random.randint(1,5) * 100 
    if type == "plane":
        enemy = EnemyPlane.EnemyPlane(random.randint(0, WINDOW_WIDTH), 0,
                    obstacle_width, obstacle_height, speed_range_x_plane, speed_range_y_plane, bullet_group, shoot_delay, all_sprite_group)
    else:
        enemy = EnemyBoat.EnemyBoat(random.randint(0, WINDOW_WIDTH), 0,
                    obstacle_width + 15, obstacle_height + 15, speed_range_x_boat, speed_range_y_boat, bullet_group, shoot_delay, all_sprite_group)
    while any(pygame.sprite.spritecollide(enemy, enemy_group, False, collided=None)):
        enemy.rect.x = random.randint(0, WINDOW_WIDTH - enemy.rect.width)
        enemy.rect.y = random.randint(0, abs(int(WINDOW_HEIGHT/10) - enemy.rect.height))
    enemy_group.add(enemy)
    all_sprite_group.add(enemy)



Enemies.groups = [enemy_group]
TIME_BEFORE_SPAWN = 1000
ENEMY_DISTANCE_THRESHOLD = 100
MAX_ENEMIES = 50
ENEMY_INTERVAL = 4000
enemy_timer = pygame.time.get_ticks()
num_enemies = 0
game_time = 0  # Total time elapsed since the start of the game
FPS = 60
obstacle_height = 50
obstacle_width = 50

current_level = "level_1"
current_difficulty = "easy"

boat_speed_max = levels["levels"][current_level][current_difficulty]["speed_max_boat"]
boat_speed_min = levels["levels"][current_level][current_difficulty]["speed_min_boat"]
plane_speed_max = levels["levels"][current_level][current_difficulty]["speed_max_plane"]
plane_speed_min = levels["levels"][current_level][current_difficulty]["speed_min_plane"]
enemy_count = levels["levels"][current_level][current_difficulty]["enemies"]
current_enemy_index = 1
current_enemy_count = enemy_count[current_enemy_index]

new_enemy = True
current_round = 0
max_round = 0

num_reset = 0


# set a variable to store the time that the delay started
# delay_start_time = pygame.time.get_ticks()


# function to display score
def display_score():
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (10, 10))
    pygame.display.update()
    
# function to display health
def display_health():
    health_text = font.render("Health: " + str(player.health), True, BLACK)
    window.blit(health_text, (WINDOW_WIDTH - 100, 10))
    pygame.display.update()
 
# rearrange sprites to give depth     
def order_depth():  
    # move player to the back of the sprite
    for sprite in all_sprite_group:
        if sprite.getType() == "player":
            all_sprite_group.move_to_back(sprite)
    # move bullets to the back of the sprite group
    for sprite in all_sprite_group:
        if sprite.getType() == "bullet":
            all_sprite_group.move_to_back(sprite)
    # move planes to the back of the sprite group
    for sprite in all_sprite_group:
        if sprite.getType() == "plane":
            all_sprite_group.move_to_back(sprite)
    # move boats to the back of the sprite group
    for sprite in all_sprite_group:
        if sprite.getType() == "boat":
            all_sprite_group.move_to_back(sprite)


######################################################################################

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
    # time_since_delay_start = pygame.time.get_ticks() - delay_start_time
    
    # Check if it's time to spawn a new enemy
    # if pygame.time.get_ticks() - enemy_timer >= ENEMY_INTERVAL and num_enemies == 0 and current_round == max_round: # and num_enemies < MAX_ENEMIES:
    if num_enemies == 0 and current_round == max_round:
        current_enemy_count = enemy_count[current_enemy_index]
        # Create a new enemy and add it to the group
        for enemy_num in range(enemy_count[current_enemy_index]):
            type = "plane"
            if random.randint(0,1):
                type = "boat"
            create_enemy(obstacle_width, obstacle_height, \
                random.randint(boat_speed_min, boat_speed_max), random.randint(boat_speed_min, boat_speed_max), \
                random.randint(plane_speed_min, plane_speed_max), random.randint(plane_speed_min, plane_speed_max), type)
            num_enemies += 1
            enemy_timer = pygame.time.get_ticks()
            random_delay = random.randint(0,2) * 100
            pygame.time.delay(random_delay)
        # move to next enemy index
        if enemy_count[current_enemy_index+1] != 100:
            current_enemy_index += 1
        current_round = 0
        max_round += 1
            
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
            if current_round < max_round:
                enemy.reset()
                num_reset += 1
                if num_reset >= current_enemy_count:
                    current_round += 1
                    
            else:
                all_sprite_group.remove(enemy)
                enemy_group.remove(enemy)
                num_enemies -= 1
                num_reset = 0
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
            all_sprite_group.remove(bullet)
            if player.health == 0:
               game_over = True
               pygame.quit() 
 
            
    for bullet in bullet_group:
        bullet.move()
        # bullet.draw()
        
    # rearrange sprites to give depth 
    order_depth()
        
    all_sprite_group.draw(window)
    
    
    display_health()
    display_score()
    
    
    
    print("round = ", current_round, "max round = ", max_round, "num_reset = ", num_reset, "current enemy count = ", current_enemy_count)
        
    
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
# better control of number of enemies on the screen over time
    # this level will be 45 seconds long and will have a max of 10 enemies on the screen. 
        # first 15 seconds: 3 enemies max on the screen
        # 5 seconds of break
        # next 15 seconds: 6 enemies on the screen
        # 5 seconds of break
        # last 15 seconds: 10 enemies on the screen
        # then tower?
# add turrels and landscape?
# add tokens?
# add towers at the end