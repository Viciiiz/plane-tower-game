import pygame
import random

# initialize pygame
pygame.init()

# game window
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
obstacle_plane_width = 50
obstacle_plane_height = 50
obstacle_boat_width = obstacle_plane_width + 10
obstacle_boat_height = obstacle_plane_height + 10
obstacle_plane_x = random.randint(0, WINDOW_WIDTH - obstacle_plane_width)
obstacle_plane_y = -obstacle_plane_height
obstacle_boat_x = random.randint(0, WINDOW_WIDTH - obstacle_boat_width)
obstacle_boat_y = -obstacle_boat_height
obstacle_speed_y = 3

game_over = False