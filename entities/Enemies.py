import random
import pygame
from my_vars.my_vars import WINDOW_WIDTH, window, BLACK, GREY


class Enemies:
    def __init__(self, x, y, width, height, speed_x, speed_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y
        if random.randint(0, 1):
            self.type = "plane"
        else:
            self.type = "boat"
        

    def move(self):
        if self.type == "plane":
            self.x += self.speed_x
            self.y += self.speed_y
        else:
            self.x += self.speed_x / 2
            self.y += self.speed_y / 2

    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height 
        if random.randint(0, 1):
            self.speed_x = random.choice([-3, 3])
        else:
            self.speed_x = 0
        self.speed_y += 0.5

    def draw(self):
        if self.type == "plane":
            pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height))
        else: 
            pygame.draw.rect(window, GREY, (self.x, self.y, self.width+10, self.height+10))
        

if __name__ == "__main__":
    my_obj = Enemies(1,1,1,1,1,1)
    my_obj.draw()