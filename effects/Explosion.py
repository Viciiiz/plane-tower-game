import pygame

# Load the explosion image
explosion_image = pygame.image.load('resources/images/explosion.png')

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = explosion_image
        
        self.type = "explosion"
        
        self.image = pygame.image.load("resources/images/explosion.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image.set_colorkey((0, 0, 0))
        self.transparent_surface = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        self.transparent_surface.fill((0, 0, 0, 0))
        self.transparent_surface.blit(self.image, (0, 0))
        self.image = self.transparent_surface
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 30
        

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()
            
    def draw(self, window):
        sprite = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sprite.blit(self.image, (0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        window.blit(self.image, self.rect)

    def getType(self):
        # return the type of the sprite
        return self.type