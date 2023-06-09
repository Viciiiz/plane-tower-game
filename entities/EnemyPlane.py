import random
import pygame
import math
from my_vars.my_vars import WINDOW_WIDTH, window, BLACK
from . import Bullet

class EnemyPlane(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, speed_x, speed_y, bullet_group, shoot_delay, all_sprite_group):
        # initialize the sprite
        pygame.sprite.Sprite.__init__(self)

        # set the position, size, and velocity of the sprite
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
        
        # assign a type to the sprite
        self.type = "plane"
        
        self.all_sprite_group = all_sprite_group

        # set the image and color of the sprite based on its type
        # self.image = pygame.Surface((width, height))
        # self.image.fill(BLACK)
        self.image = pygame.image.load("resources/images/enemy-plane.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.set_colorkey((0, 0, 0))
        self.transparent_surface = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        self.transparent_surface.fill((0, 0, 0, 0))
        self.transparent_surface.blit(self.image, (0, 0))
        self.image = self.transparent_surface
        
        # self.velocity = [speed_x, speed_y]
        
        # create a timer for shooting
        self.shoot_timer = 0
        self.shoot_delay = shoot_delay # milliseconds
        
        self.bullet_group = bullet_group
        
        # Create a mask for the image
        self.image_copy = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image_copy)
            

    def move(self, player_pos):
        # update the position of the sprite based on its velocity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # # Update the sprite's position based on its velocity
        # self.rect.move_ip(*self.velocity)

        # # Calculate the angle of rotation based on the sprite's velocity
        # angle = math.atan2(self.velocity[1], self.velocity[0])
        # angle_degrees = math.degrees(angle)

        # # Rotate the sprite's image
        # self.image = pygame.transform.rotate(self.transparent_surface, -angle_degrees-90)
        self.image = pygame.transform.rotate(self.transparent_surface, -180)
        # self.rect = self.image.get_rect(center=self.rect.center)
        
         # Update the mask for the rotated image
        self.mask = pygame.mask.from_surface(self.image)

            
        # check if it's time to shoot
        now = pygame.time.get_ticks()
        # player_pos = (0, 0)
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_at_player(player_pos)
            self.shoot_timer = now


    def shoot(self):
        # create a new bullet instance and add it to the bullet group
        bullet = Bullet.Bullet(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height, self.speed_y + 2, 5)
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
        # pygame.draw.rect(window, BLACK, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        sprite = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sprite.blit(self.image, (0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        window.blit(self.image, self.rect)

    def getType(self):
        # return the type of the sprite
        return self.type
    
    def setShootDelay(self, shoot_delay):
        self.shoot_delay = shoot_delay
    
