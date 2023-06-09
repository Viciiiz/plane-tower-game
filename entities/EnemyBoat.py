import random
import pygame
import math
from my_vars.my_vars import WINDOW_WIDTH, window, GREY
from . import Bullet

class EnemyBoat(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, speed_x, speed_y, bullet_group, shoot_delay, all_sprite_group):
        # initialize the sprite
        pygame.sprite.Sprite.__init__(self)

        # set the position, size, and velocity of the sprite
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = speed_x 
        self.speed_y = speed_y 
        
        self.all_sprite_group = all_sprite_group
        
        # assign a type to the sprite
        self.type = "boat"

        # set the image and color of the sprite based on its type
        # self.image = pygame.Surface((width, height))
        
        # self.image.fill(GREY)
            
        # create a timer for shooting
        self.shoot_timer = 0
        self.shoot_delay = shoot_delay # milliseconds
        
        self.bullet_group = bullet_group
        
        self.image = pygame.image.load("resources/images/enemy-boat.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.set_colorkey((0, 0, 0))
        self.transparent_surface = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        self.transparent_surface.fill((0, 0, 0, 0))
        self.transparent_surface.blit(self.image, (0, 0))
        self.image = self.transparent_surface
            

    def move(self, player_pos):
        # update the position of the sprite based on its velocity
        self.rect.x += self.speed_x / 2
        self.rect.y += self.speed_y / 2
            
        # check if it's time to shoot
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_at_player(player_pos)
            self.shoot_timer = now


    def shoot(self):
        # create a new bullet instance and add it to the bullet group
        bullet = Bullet.Bullet(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height, 1, self.speed_y + 3, 5)
        self.bullet_group.add(bullet)
        self.all_sprite_group.add(bullet)
        
        
    def shoot_at_player(self, player_pos):
        # calculate the angle between the enemy and the player
        dx = player_pos[0] - (self.rect.x + self.rect.width / 2)
        dy = player_pos[1] - (self.rect.y + self.rect.height / 2)
        angle = math.atan2(dy, dx)
        
        # calculate the velocity vector for the bullet
        speed = 5
        bullet_speed_x = speed * math.cos(angle)
        bullet_speed_y = speed * math.sin(angle)
        
        # create a new bullet instance and add it to the bullet group
        bullet = Bullet.Bullet(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height, bullet_speed_x, bullet_speed_y, 5)
        self.bullet_group.add(bullet)
        self.all_sprite_group.add(bullet)
            

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
        # pygame.draw.rect(window, GREY, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        sprite = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sprite.blit(self.image, (0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        window.blit(self.image, self.rect)
            

    def getType(self):
        # return the type of the sprite
        return self.type
    
    def setShootDelay(self, shoot_delay):
        self.shoot_delay = shoot_delay
    
