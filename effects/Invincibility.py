import pygame

from my_vars.my_vars import RED, window

class Invincibility(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.Surface((player_rect.width+5, player_rect.height+5))
        self.image.fill((0, 255, 0, 100)) # green semi-transparent color
        self.rect = player_rect.copy()
        self.original_rect = player_rect
        self.window = window

    def update(self):
        # move the effect with the player
        self.rect.center = self.original_rect.center
        
        
    def draw(self):
        # draw the player on the given surface
        pygame.draw.rect(self.window, RED, self.rect)