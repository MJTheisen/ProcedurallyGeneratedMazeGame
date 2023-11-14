import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 820, 620
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
START_POS = (1, 1)
FINISH_POS = (ROWS - 2, COLS - 2)

# Create maze
maze = [['wall' for _ in range(COLS)] for _ in range(ROWS)]

def is_valid(x, y):
    return 0 <= x < ROWS and 0 <= y < COLS and maze[x][y] == 'path'

def carve_path(x, y):
    maze[x][y] = 'path'

    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 'wall':
            maze[(x + nx) // 2][(y + ny) // 2] = 'path'
            carve_path(nx, ny)

carve_path(START_POS[0], START_POS[1])

# Initialize player position
player_pos = list(START_POS)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedurally Generated Maze Game")

# Font setup
font_size = 48  # Adjust the font size
font = pygame.font.Font(None, font_size)
congratulations_text = font.render("Congratulations you won!", True, (100, 216, 230))  # Pale light blue
congratulations_rect = congratulations_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

play_again_text = font.render("Play again? 'Y' , or quit? 'Q' ", True, (100, 216, 230))  # Pale light blue
play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + font_size))
y_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))


def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if maze[row][col] == 'wall' else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_finish():
    row, col = FINISH_POS
    if maze[row][col] == 'path':
        pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player():
    pygame.draw.rect(screen, GREEN, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Main loop
clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and is_valid(player_pos[0] - 1, player_pos[1]):
        player_pos[0] -= 1
    elif keys[pygame.K_DOWN] and is_valid(player_pos[0] + 1, player_pos[1]):
        player_pos[0] += 1
    elif keys[pygame.K_LEFT] and is_valid(player_pos[0], player_pos[1] - 1):
        player_pos[1] -= 1
    elif keys[pygame.K_RIGHT] and is_valid(player_pos[0], player_pos[1] + 1):
        player_pos[1] += 1

    if tuple(player_pos) == FINISH_POS:
        screen.fill(WHITE)
        draw_maze()
        draw_finish()
        draw_player()

        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Adjust the alpha value for transparency
        screen.blit(overlay, (0, 0))


        screen.blit(congratulations_text, congratulations_rect)
        screen.blit(play_again_text, play_again_rect)
        pygame.display.flip()

        # Allow player to choose to play again or quit
        choice = None
        while choice not in ['y', 'q']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        choice = 'y'
                    elif event.key == pygame.K_q:
                        choice = 'q'

        if choice == 'y':
            game_over = False
            player_pos = list(START_POS)
            # Generate a new maze
            maze = [['wall' for _ in range(COLS)] for _ in range(ROWS)]
            carve_path(START_POS[0], START_POS[1])
        else:
            game_over = True

        pygame.time.delay(2000)  # Display the message for 2 seconds

    else:
        screen.fill(WHITE)
        draw_maze()
        draw_finish()
        draw_player()
        pygame.display.flip()

    clock.tick(20)  # Limit the frames per second