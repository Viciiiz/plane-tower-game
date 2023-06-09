import random
import pygame
from my_vars.my_vars import WINDOW_WIDTH, window, BLACK, GREY
from . import Bullet

class Enemies(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, speed_x, speed_y, type, bullet_group, shoot_delay):
        # initialize the sprite
        pygame.sprite.Sprite.__init__(self)

        # set the position, size, and velocity of the sprite
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
        
        # assign a type to the sprite
        self.type = type

        # set the image and color of the sprite based on its type
        self.image = pygame.Surface((width, height))
        if self.type == "plane":
            self.image.fill(BLACK)
        else:
            self.image.fill(GREY)
            
        # create a timer for shooting
        self.shoot_timer = 0
        self.shoot_delay = shoot_delay # milliseconds
        
        self.bullet_group = bullet_group
            

    def move(self):
        # update the position of the sprite based on its velocity
        if self.type == "plane":
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        else:
            self.rect.x += self.speed_x / 2
            self.rect.y += self.speed_y / 2
            
        # check if it's time to shoot
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot()
            self.shoot_timer = now

    def shoot(self):
        # create a new bullet instance and add it to the bullet group
        bullet = Bullet.Bullet(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height, 5, 5)
        self.bullet_group.add(bullet)
            

    def reset(self):
        # reset the position and velocity of the sprite
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        if random.randint(0, 1):
            self.speed_x = random.choice([-3, 3])
        else:
            self.speed_x = 0
        self.speed_y += 0.3
        
        
    def draw(self):
        if self.type == "plane":
            pygame.draw.rect(window, BLACK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        else: 
            pygame.draw.rect(window, GREY, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
            

    def getType(self):
        # return the type of the sprite
        return self.type
    
    def setShootDelay(self, shoot_delay):
        self.shoot_delay = shoot_delay
    
