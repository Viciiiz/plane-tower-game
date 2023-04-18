import random
import pygame
from my_vars.my_vars import WINDOW_WIDTH, window, BLACK


class Enemies:
    def __init__(self, x, y, width, height, speed_x, speed_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height
        if random.randint(0, 1):
            self.speed_x = random.choice([-3, 3])
        else:
            self.speed_x = 0
        self.speed_y += 0.5

    def draw(self):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height))
        

if __name__ == "__main__":
    my_obj = Enemies(1,1,1,1,1,1)
    my_obj.draw()