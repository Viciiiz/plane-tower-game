import pygame
from my_vars.my_vars import window, RED

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed_x, speed_y, radius):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, radius*2, radius*2)
        self.speed_y = speed_y
        self.speed_x = speed_x
        
        self.type = "bullet"
        
        self.radius = radius

        # create the image for the sprite
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)

    def move(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # destroy the bullet if it goes off the screen
        if self.rect.bottom < 0:
            self.kill()

    def draw(self):
        pygame.draw.rect(window, RED, self.rect)
        
    def getType(self):
        # return the type of the sprite
        return self.type
