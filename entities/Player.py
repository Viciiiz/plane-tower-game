import pygame
from my_vars.my_vars import WINDOW_WIDTH, window, BLACK, GREY, WINDOW_WIDTH, WINDOW_HEIGHT, window, BLACK, WHITE, PLAYER_WIDTH, PLAYER_HEIGHT, \
    player_speed, font, score, obstacle_plane_width, obstacle_plane_height, obstacle_boat_width, obstacle_boat_height, \
        obstacle_plane_x, obstacle_plane_y, obstacle_boat_x, obstacle_boat_y, game_over

# class Player(pygame.sprite.Sprite):
    
#     def __init__(self, player_x, player_y):
#         pygame.sprite.Sprite.__init__(self)

#         self.rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
#         # self.speed_y = speed_y
        
#         self.player_x = player_x
#         self.player_y = player_y
        

#         self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
#         self.image.fill(BLACK)
#         self.health = 5
        

#     def move(self):
#         # handle player movement
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT] and self.player_x > 0:
#             self.player_x -= player_speed
#         if keys[pygame.K_RIGHT] and self.player_x < WINDOW_WIDTH - PLAYER_WIDTH:
#             self.player_x += player_speed
#         if keys[pygame.K_DOWN] and self.player_y < WINDOW_HEIGHT - PLAYER_WIDTH:
#             self.player_y += player_speed
#         if keys[pygame.K_UP] and self.player_y > 0:
#             self.player_y -= player_speed

#     def draw(self):
#         pygame.draw.rect(window, BLACK, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        # initialize the sprite
        pygame.sprite.Sprite.__init__(self)

        # set the position, size, and velocity of the sprite
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

        # set the image and color of the sprite
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        
        self.health = 5

    def move(self, keys):
        # update the position of the sprite based on user input
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # make sure the sprite stays within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            
    def draw(self):
        # draw the player on the given surface
        pygame.draw.rect(window, BLACK, self.rect)