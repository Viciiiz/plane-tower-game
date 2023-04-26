import random
import pygame
from my_vars.my_vars import WINDOW_WIDTH, WINDOW_HEIGHT, GREEN

class Token(pygame.sprite.Sprite):
    
    def __init__(self, all_sprite_group):
        # initialize the sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.all_sprite_group = all_sprite_group

        # set the position, size, and velocity of the sprite
        self.rect = pygame.Rect(random.randint(0, WINDOW_WIDTH - 10), -10, 10, 10)
        self.speed_y = 2
        
        # assign a type to the sprite
        rand_category = random.randint(1,10)
        if rand_category == 8:
            self.category = "life"
        elif rand_category == 2:
            self.category = "boost"
        else:
            self.category = "score"
            
        self.type = "token"

        # set the image and color of the sprite based on its type
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)

        # create a timer for the coin to respawn
        self.respawn_timer = 0
        self.respawn_delay = 15000 # 15 seconds in milliseconds
        
    def move(self):
        # update the position of the sprite based on its velocity
        self.rect.y += self.speed_y
        
        # check if the coin has gone off the screen
        if self.rect.y > WINDOW_HEIGHT:
            self.reset()
            # self.kill()
        
    def draw(self, window):
        pygame.draw.rect(window, GREEN, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        
    def reset(self):
        # reset the position and velocity of the sprite and start the respawn timer
        self.rect.x = random.randint(0, WINDOW_WIDTH - 10)
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

