import math
import pygame
import random
from entities import Enemies, Player, EnemyBoat, EnemyPlane, Tokens, Towers, man, RedEyes
from effects import Invincibility, Explosion
import json
# from game.level import levels
from my_vars.my_vars import WINDOW_WIDTH, WINDOW_HEIGHT, window, BLACK, WHITE, ASPHALT, BEACH, CLEAR_BLUE, PLAYER_WIDTH, PLAYER_HEIGHT, player_x, player_y, \
    player_speed, font, score, obstacle_plane_width, obstacle_plane_height, obstacle_boat_width, obstacle_boat_height, \
        obstacle_plane_x, obstacle_plane_y, obstacle_boat_x, obstacle_boat_y, game_over


pygame.display.set_caption("Unmask the Politician")

pygame.mixer.init()

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
all_sprite_group = pygame.sprite.LayeredUpdates()
token_group = pygame.sprite.Group()
player_invincibility_effect_group = pygame.sprite.Group()
explosions = pygame.sprite.Group()


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
                    obstacle_width + 15, obstacle_height + 100, speed_range_x_boat, speed_range_y_boat, bullet_group, shoot_delay, all_sprite_group)
    while any(pygame.sprite.spritecollide(enemy, enemy_group, False, collided=None)):
        enemy.rect.x = random.randint(0, WINDOW_WIDTH - enemy.rect.width)
        enemy.rect.y = random.randint(0, abs(int(WINDOW_HEIGHT/10) - enemy.rect.height))
    enemy_group.add(enemy)
    all_sprite_group.add(enemy)



Enemies.groups = [enemy_group]
TIME_BEFORE_SPAWN = 1000
ENEMY_DISTANCE_THRESHOLD = 200
MAX_ENEMIES = 50
ENEMY_INTERVAL = 4000
TOKEN_DELAY = 4000
current_token_delay = TOKEN_DELAY
enemy_timer = pygame.time.get_ticks()
num_enemies = 0
game_time = 0  # Total time elapsed since the start of the game
FPS = 60
obstacle_height = 100
obstacle_width = 100

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

player_invincibility = 0
using_invincibility = False

is_on_ocean = True

# set a variable to store the time that the delay started
delay_start_time = pygame.time.get_ticks()


# function to display score
def display_score():
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (15, 10))
    pygame.display.update()
    
# function to display health
def display_health():
    health_text = font.render("Health: " + str(player.health), True, BLACK)
    window.blit(health_text, (15, 40))
    pygame.display.update()
    
# function to display health
def display_invincibility():
    health_text = font.render("Invincibility: " + str(player_invincibility), True, BLACK)
    window.blit(health_text, (WINDOW_WIDTH - 160, 10))
    pygame.display.update()
 
# rearrange sprites to give depth     
def order_depth():  
    # move tokens to the back of the sprite group
    for sprite in all_sprite_group:
        if sprite.getType() == "token":
            all_sprite_group.move_to_back(sprite)
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
    # move boats to the back of the sprite group
    for sprite in all_sprite_group:
        if sprite.getType() == "tower":
            all_sprite_group.move_to_back(sprite)
            

# Define the top and bottom colors of the gradient
top_color = BEACH
bottom_color = CLEAR_BLUE
top_color_2 = ASPHALT
bottom_color_2 = BEACH

# Create a surface for the gradient
gradient_surface = pygame.Surface((window.get_width(), window.get_height()))

# Draw the gradient on the surface
for y in range(window.get_height()):
    # Calculate the color at this point in the gradient
    t = y / (window.get_height() - 1)
    color = tuple(int((1 - t) * c1 + t * c2) for c1, c2 in zip(top_color, bottom_color))

    # Draw a line of this color on the surface
    pygame.draw.line(gradient_surface, color, (0, y), (window.get_width(), y))

tower = Towers.Tower(WINDOW_WIDTH/2,0,100,1000)
man = man.Man(int(WINDOW_WIDTH/8),0,500,700)
redEyes = RedEyes.RedEyes(int(WINDOW_WIDTH/8),0,500,700)
######################################################################################

# game loop
while not game_over:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            # invincibility
            if event.key == pygame.K_SPACE:
                if player_invincibility > 0:
                    player.activate_invincibility_effect()
                    player_invincibility -= 1
                    player_invincibility_effect_group.add(Invincibility.Invincibility(player.rect))
                    player.set_effect_start_time(pygame.time.get_ticks())
        if event.type == pygame.USEREVENT and player.is_invincible:
            # timer has expired
            player.deactivate_invincibility_effect()
            player_invincibility_effect_group.empty()
            
    game_time += clock.tick(FPS)
    
    current_enemy_count = enemy_count[current_enemy_index]
    
    if current_enemy_count == 100:
        # while(1):
        
        tower.draw()
        all_sprite_group.empty()
        player_group.empty()
        enemy_group.empty()
        bullet_group.empty()
        token_group.empty()
        all_sprite_group.add(tower)
        all_sprite_group.move_to_back(tower)
        all_sprite_group.add(man)
        all_sprite_group.remove(redEyes)
        if player.collides_with(tower):
            # Create an explosion at the position of the other sprite
            explosion = Explosion.Explosion(player.rect.centerx, player.rect.centery)
            all_sprite_group.add(explosion)
            all_sprite_group.add(redEyes)
            explosion_sound = pygame.mixer.Sound('resources/audio/explosion.flac')
            explosion_sound.play()
            explosions.add(explosion)
    
        

    window.fill(CLEAR_BLUE)
    
            
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
    player_invincibility_effect_group.update()
    player.draw() 
    player_invincibility_effect_group.draw(window)
    
    
            
    # check how much time has passed since the delay started
    time_since_delay_start = pygame.time.get_ticks() - delay_start_time
    # print(" ", current_token_delay, " ", time_since_delay_start, " ", delay_start_time)
    # create a new token instance 
    if time_since_delay_start >= (delay_start_time + current_token_delay) and len(token_group) == 0 and current_enemy_count != 100:
        token = Tokens.Token(all_sprite_group)
        token_group.add(token)
        # all_sprite_group.add(token)
        
    if len(token_group) > 0:
        # update and draw the coin
        token.move()
        token.draw(window)
 
            
        # check for collisions with the player
        if token.checkCollision(player):
            # time_since_delay_start = 0
            print(token.getCategory())
            if token.getCategory() == "score":
                score += 100
            elif token.getCategory() == "life":
                player.health += 1
            else:
                player_invincibility += 1
                
            token_group.remove(token)
            all_sprite_group.remove(token)
            token.kill()
            delay_start_time = time_since_delay_start
            rand_token_generation = random.randint(1,4) * 1000
            if random.randint(0,1):
                # print("subtracting delay", current_token_delay, " ", time_since_delay_start)
                current_token_delay = TOKEN_DELAY - rand_token_generation
            else:
                # print("adding delay", current_token_delay, " ", time_since_delay_start)
                current_token_delay = TOKEN_DELAY + rand_token_generation
                
        
    
    # Check if it's time to spawn a new enemy
    # if pygame.time.get_ticks() - enemy_timer >= ENEMY_INTERVAL and num_enemies == 0 and current_round == max_round: # and num_enemies < MAX_ENEMIES:
    if num_enemies == 0 and current_round == max_round and current_enemy_count != 100:
        current_enemy_count = enemy_count[current_enemy_index]
        # Create a new enemy and add it to the group
        for enemy_num in range(enemy_count[current_enemy_index]):
            type = "plane"
            if random.randint(0,1) and is_on_ocean:
                type = "boat"
            create_enemy(obstacle_width, obstacle_height, \
                random.randint(boat_speed_min, boat_speed_max), random.randint(boat_speed_min, boat_speed_max), \
                random.randint(plane_speed_min, plane_speed_max), random.randint(plane_speed_min, plane_speed_max), type)
            num_enemies += 1
            enemy_timer = pygame.time.get_ticks()
            # random_delay = random.randint(0,2) * 1000
            # pygame.time.delay(random_delay)
        # move to next enemy index
        # if enemy_count[current_enemy_index+1] != 100:
        current_enemy_index += 1
        current_round = 0
        max_round += 1
            
    # move enemies
    for enemy in enemy_group:
        enemy.move(player.rect.center)
        
        # make sure the enemies don't overlap if they are the same type
        for other_enemy in enemy_group:
            if enemy != other_enemy and (enemy.getType() == "boat" and other_enemy.getType() == "boat"):
                dx = enemy.rect.x - other_enemy.rect.x
                dy = enemy.rect.y - other_enemy.rect.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < ENEMY_DISTANCE_THRESHOLD:
                    # if two enemies are too close, move one of them away
                    angle = math.atan2(dy, dx)
                    enemy.rect.x += math.cos(angle) * (ENEMY_DISTANCE_THRESHOLD - distance) / 2
                    enemy.rect.y += math.sin(angle) * (ENEMY_DISTANCE_THRESHOLD - distance) / 2
                    break
            elif enemy != other_enemy and (enemy.getType() == "boat" and other_enemy.getType() == "boat"): 
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
    
    if not player.getInvincibilityStatus():
        # handle collision detection between enemies and player
        player_collisions = pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_mask)
        for enemy in player_collisions:
            # Check if the masks overlap
            if pygame.sprite.collide_mask(player, enemy) and enemy.getType() == "plane":
                # Create an explosion at the position of the other sprite
                explosion = Explosion.Explosion(player.rect.centerx, player.rect.centery)
                explosion.draw(window)
                explosions.add(explosion)
                explosion_sound = pygame.mixer.Sound('resources/audio/explosion.flac')
                explosion_sound.play()
                game_over = True  
               
        # handle collision between player and bullet 
        bullet_collisions = pygame.sprite.spritecollide(player, bullet_group, False, pygame.sprite.collide_mask)
        for bullet in bullet_collisions:
            # Check if the masks overlap
            if pygame.sprite.collide_mask(player, bullet):
                player.health -= 1
                explosion_sound = pygame.mixer.Sound('resources/audio/impact.wav')
                explosion_sound.play()

                bullet_group.remove(bullet)
                all_sprite_group.remove(bullet)
                if player.health == 0:
                    # Create an explosion at the position of the other sprite
                    explosion = Explosion.Explosion(player.rect.centerx, player.rect.centery)
                    explosion.draw(window)
                    explosions.add(explosion)
                    game_over = True
                
    # In your draw function:
    explosions.update()
    explosions.draw(window)
            
    for bullet in bullet_group:
        bullet.move()
        # bullet.draw()
        
    # rearrange sprites to give depth 
    order_depth()
        
    all_sprite_group.draw(window)
    
    
    display_health()
    display_score()
    display_invincibility()
    
    
    
    # print("round = ", current_round, "max round = ", max_round, "num_reset = ", num_reset, "current enemy count = ", current_enemy_count)


    # set the game's FPS
    clock.tick(FPS)

# quit pygame
pygame.quit()
