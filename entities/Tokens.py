import random
import pygame
# import sys
# sys.path.insert(0, '../')
# from my_vars.my_vars import WINDOW_WIDTH, WINDOW_HEIGHT, GREEN

class Token(pygame.sprite.Sprite):
    
    def __init__(self, all_sprite_group):
        # initialize the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.all_sprite_group = all_sprite_group

        # set the position, size, and velocity of the sprite
        self.rect = pygame.Rect(random.randint(0, 900 - 10), -10, 10, 10)
        self.speed_y = 2
        
        # assign a type to the sprite
        rand_category = random.randint(1,10)
        if rand_category > 8:
            self.category = "life"
            self.image = pygame.image.load("resources/images/heart.png").convert_alpha()
        elif rand_category < 4:
            self.category = "invincibility"
            self.image = pygame.image.load("resources/images/boost.png").convert_alpha()
        else:
            self.category = "score"
            self.image = pygame.image.load("resources/images/star.png").convert_alpha()
            
        
        
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.image.set_colorkey((0, 0, 0))
        self.transparent_surface = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        self.transparent_surface.fill((0, 0, 0, 0))
        self.transparent_surface.blit(self.image, (0, 0))
        self.image = self.transparent_surface
            
        self.type = "token"

        # set the image and color of the sprite based on its type
        # self.image = pygame.Surface((10, 10))
        # self.image.fill(GREEN)

        # create a timer for the coin to respawn
        self.respawn_timer = 0
        self.respawn_delay = 15000 # 15 seconds in milliseconds
        
    def move(self):
        # update the position of the sprite based on its velocity
        self.rect.y += self.speed_y
        
        # check if the coin has gone off the screen
        if self.rect.y > 700:
            self.reset()
            # self.kill()
        
    def draw(self, window):
        # pygame.draw.rect(window, GREEN, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        sprite = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sprite.blit(self.image, (0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        window.blit(self.image, self.rect)
        
    def reset(self):
        # reset the position and velocity of the sprite and start the respawn timer
        self.rect.x = random.randint(0, 900 - 10)
        self.rect.y = -10
        self.speed_y = 2
        self.respawn_timer = pygame.time.get_ticks()
        
    def getType(self):
        # return the type of the sprite
        return self.type

    def checkCollision(self, player):
        # check if the coin has collided with the player
        if self.rect.colliderect(player.rect):
            #self.reset()
            return True
        return False
        
    def shouldRespawn(self):
        # check if it's time for the coin to respawn
        now = pygame.time.get_ticks()
        if now - self.respawn_timer > self.respawn_delay:
            return True
        return False
    
    def getType(self):
        # return the type of the sprite
        return self.type
    
    def getCategory(self):
        # return the category of the sprite
        return self.category

