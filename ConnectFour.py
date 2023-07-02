import pygame
import sys
from pygame.locals import QUIT
import time

#Board Image: https://studio.code.org/v3/assets/TLFZogscaPiUKUzLFfvzYQ/Connect4Board.png

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BOARD_X = 80
BOARD_Y = 120
BOARD_WIDTH = 640
BOARD_HEIGHT= 480
BOARD_BORDER = 2

ROWS = 6
COLUMNS = 7
BOTTOM_ROW_Y = 561

INITIAL_Y = 70
INITIAL_X = 130
X_STEP = 90
Y_STEP = 80

CIRCLE_RADIUS = 35

RED = (255, 0, 0)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_circle(color, pos):
    pygame.draw.circle(screen, color, pos, CIRCLE_RADIUS)

def place_update(x_pos):
    global piece_color, pieces, colors
    current_column = int((x_pos-INITIAL_Y)/X_STEP)
    if current_column >= 0 and current_column < COLUMNS and pieces[current_column][ROWS - 1] != 1:
        for current_row in range(ROWS):
            if pieces[current_column][current_row] == 0:
                pieces[current_column][current_row] = 1
                colors[current_column][current_row] = piece_color
                break
    else:
      piece_color = YELLOW if piece_color == RED else RED

def check_winner():
    #horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if colors[col][row] == colors[col+1][row] == colors[col+2][row] == colors[col+3][row] != 0:
                return colors[col][row]
    #vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if colors[col][row] == colors[col][row+1] == colors[col][row+2] == colors[col][row+3] != 0:
                return colors[col][row]
    #diagonal check
    for row in range(ROWS - 1, ROWS - 4, -1):
        for col in range(COLUMNS - 3):
            if colors[col][row] == colors[col+1][row-1] == colors[col+2][row-2] == colors[col+3][row-3] != 0:
                return colors[col][row]

    #diagonal check
    for row in range(ROWS - 1, ROWS - 4 , -1):
        for col in range(COLUMNS - 1, COLUMNS - 4, -1):
            if colors[col][row] == colors[col-1][row-1] == colors[col-2][row-2] == colors[col-3][row-3] != 0:
                return colors[col][row]
    return False
    

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect Four")

board_image = pygame.image.load("Connect4Board.png")

#0 if piece isn't there, 1 if piece is there
pieces = [[0 for i in range(ROWS)] for j in range(COLUMNS)]

#the colors 2D array allows the retrieval of piece color at a specific index
colors = [[0 for i in range(ROWS)] for j in range(COLUMNS)]

current_x = INITIAL_X
piece_color = RED

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and current_x < ROWS*X_STEP + INITIAL_X:
                current_x += X_STEP
            if event.key == pygame.K_LEFT and current_x > INITIAL_X:
                current_x -= X_STEP
            if event.key == pygame.K_DOWN:
                place_update(current_x)
                piece_color = YELLOW if piece_color == RED else RED

    #clears screen
    screen.fill(WHITE)

    #draw board (includes borders)
    screen.blit(board_image, (BOARD_X, BOARD_Y))
    for i in range(COLUMNS):
        for j in range(ROWS):
            pygame.draw.circle(screen, BLACK, ((INITIAL_X + i*X_STEP), (BOTTOM_ROW_Y-(Y_STEP*j))), CIRCLE_RADIUS + BOARD_BORDER, BOARD_BORDER)
    pygame.draw.rect(screen, BLACK, pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), BOARD_BORDER)

    #draw coins
    draw_circle(piece_color, (current_x, INITIAL_Y))

    for i in range(COLUMNS):
        for j in range(ROWS):
            if pieces[i][j] == 1:
                draw_circle(colors[i][j], ((INITIAL_X + i*X_STEP), (BOTTOM_ROW_Y-(Y_STEP*j))))

    pygame.display.flip()

    #checks for winner
    if check_winner() == RED:
        print("Red Won")
        time.sleep(0.5)
        pygame.quit()
        sys.exit()
    elif check_winner() == YELLOW:
        print("Yellow Won")
        time.sleep(0.5)
        pygame.quit()
        sys.exit()
