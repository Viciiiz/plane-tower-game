import pygame
from my_vars.my_vars import window, RED

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, speed_y, radius):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, radius*2, radius*2)
        self.speed_y = speed_y
        
        self.radius = radius

        # create the image for the sprite
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)

    def move(self):
        self.rect.y += self.speed_y
        
        # destroy the bullet if it goes off the screen
        if self.rect.bottom < 0:
            self.kill()

    def draw(self):
        pygame.draw.rect(window, RED, self.rect)
