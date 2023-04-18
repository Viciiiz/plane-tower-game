import pygame
import random

# initialize pygame
pygame.init()

# game window
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# player and player's movement speed
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
player_x = (WINDOW_WIDTH - PLAYER_WIDTH) // 2
player_y = WINDOW_HEIGHT - PLAYER_HEIGHT - 10
player_speed = 5

# set up the font for displaying the score
font = pygame.font.SysFont(None, 30)

# score
score = 0

# obstacle and obstacle's movement speed
obstacle_width = 50
obstacle_height = 50
obstacle_x = random.randint(0, WINDOW_WIDTH - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed_y = 3
