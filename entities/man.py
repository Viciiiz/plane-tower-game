import pygame
from my_vars.my_vars import WINDOW_WIDTH, window, BLUE, RED, WINDOW_WIDTH, WINDOW_HEIGHT, window, BLACK, WHITE, PLAYER_WIDTH, PLAYER_HEIGHT, \
    player_speed, font, score, obstacle_plane_width, obstacle_plane_height, obstacle_boat_width, obstacle_boat_height, \
        obstacle_plane_x, obstacle_plane_y, obstacle_boat_x, obstacle_boat_y, game_over


class Man(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        # initialize the sprite
        pygame.sprite.Sprite.__init__(self)

        # set the position, size, and velocity of the sprite
        self.rect = pygame.Rect(x, y, width, height)
        
        self.type = "man"

        # set the image and color of the sprite
        # # pygame.image.load("resources/images/plane-top.jpg")
        # self.image = pygame.image.load("resources/images/plane-top.png").convert_alpha()
        # self.mask = pygame.mask.from_surface(self.image)
        # # self.image.set_colorkey((255, 255, 255))
        # self.image = pygame.transform.scale(self.image, (width, height))
        # # self.image = pygame.Surface((width, height))
        # # self.image.fill(BLUE)
        self.image = pygame.image.load("resources/images/man.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 500))
        self.image.set_colorkey((0, 0, 0))
        self.transparent_surface = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        self.transparent_surface.fill((0, 0, 0, 0))
        self.transparent_surface.blit(self.image, (0, 0))
        self.image = self.transparent_surface
        # self.rect = self.image.get_rect()
        
        self.health = 5
        self.is_invincible = False
        
        # cooldown bar surface for invincibility effect
        # self.cooldown_bar = pygame.Surface((width, 5))
        # self.cooldown_bar.fill(RED)
        self.cooldown_bar_width = width+100
        self.cooldown_bar_height = 5
        self.cooldown_bar_color = BLUE
        self.cooldown_bar = pygame.Surface((self.cooldown_bar_width, self.cooldown_bar_height))
        self.cooldown_bar.fill(self.cooldown_bar_color)
        
        self.effect_start_time = 0
        
        # Create a mask for the image
        self.image_copy = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image_copy)

            
    def draw(self):
        # draw the player on the given surface
        # pygame.draw.rect(window, BLACK, self.rect)
        sprite = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sprite.blit(self.image, (0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        window.blit(self.image, self.rect)
        # decrease the size of the cooldown bar as the effect timer counts down
        # if self.is_invincible:
        #     time_left = pygame.time.get_ticks() - self.effect_start_time
        #     if time_left >= 0:
        #         time_passed = min(time_left, 4000)
        #         self.cooldown_bar_width = int((1 - time_passed / 4000) * self.rect.width)
        #         self.cooldown_bar = pygame.Surface((self.cooldown_bar_width, self.cooldown_bar_height))
        #         self.cooldown_bar.fill(BLUE)

        #         if time_left >= 4000:
        #             self.effect_active = False
        #             pygame.time.set_timer(pygame.USEREVENT, 0)
        # # draw the cooldown bar above the player's sprite
        # if self.is_invincible:
        #     window.blit(self.cooldown_bar, (self.rect.left, self.rect.top - 10))
        
    def activate_invincibility_effect(self):
        self.is_invincible = True
        pygame.time.set_timer(pygame.USEREVENT, 4000)
        # self.image.fill(RED)
        # reset the cooldown bar to full size
        self.cooldown_bar_size = self.rect.width
        self.cooldown_bar = pygame.Surface((self.cooldown_bar_size, 5))
        self.cooldown_bar.fill(RED)
        
        
    def deactivate_invincibility_effect(self):
        self.is_invincible = False
        pygame.time.set_timer(pygame.USEREVENT, 0)
        # self.image.fill(BLUE)
        
    def getType(self):
        # return the type of the sprite
        return self.type
    
    def getPosition(self):
        return self.rect.top - int(self.rect.height/2), self.rect.right - int(self.rect.width/2) 
    
    def getInvincibilityStatus(self):
        return self.is_invincible
    
    def set_effect_start_time(self, time):
        self.effect_start_time = time
        
    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y
