import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // ROWS

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

DARK_BROWN = (101, 67, 33)  # Dark wood color
LIGHT_CREAM = (255, 248, 220)  # Cream color

BOARD_DARK = DARK_BROWN
BOARD_LIGHT = LIGHT_CREAM

PLAYER1_COLOR = BLACK  # Replace BLUE with BLACK
PLAYER2_COLOR = RED    # Replace WHITE with RED

try:
    CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44, 25))
except:
    CROWN = None
    print("Warning: Crown image not found!")
