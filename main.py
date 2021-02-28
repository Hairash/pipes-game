import pygame
import math
# Initializing Pygame
pygame.init()

# Screen
WINDOW_SIZE = 500
ROWS = 10
CELL_SIZE = WINDOW_SIZE // ROWS
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Pipes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (CELL_SIZE, CELL_SIZE))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.jpg"), (CELL_SIZE, CELL_SIZE))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

# Global variables
global field_matrix

# State
drag = False
prev_cell = None


def draw_grid():
    # Starting points
    x = 0
    y = 0

    window.fill(WHITE)
    for i in range(ROWS):
        x = i * CELL_SIZE
        pygame.draw.line(window, GRAY, (x, 0), (x, WINDOW_SIZE), 3)
        pygame.draw.line(window, GRAY, (0, x), (WINDOW_SIZE, x), 3)

    pygame.display.update()


def initialize_game_array():
    """Initializing field matrix
    Field legenda:
    0 - empty cell
    1 - filled cell
    """
    global field_matrix
    field_matrix = [[0] * ROWS for _ in range(ROWS)]


def coordinates_to_cell(x, y):
    cell_x = x // CELL_SIZE
    cell_y = y // CELL_SIZE
    return cell_x, cell_y


def cell_image_coordinates(cell_x, cell_y):
    x = CELL_SIZE * cell_x
    y = CELL_SIZE * cell_y
    return x, y


def fill_cell(cell_x, cell_y):
    x, y = cell_image_coordinates(cell_x, cell_y)
    window.blit(X_IMAGE, (x, y))
    pygame.display.update()


def change_cell(cell_x, cell_y, value):
    # TODO: add case value
    fill_cell(cell_x, cell_y)
    field_matrix[cell_x][cell_y] = value


def mouse_move():
    global prev_cell
    if not drag:
        return
    mouse_pos = pygame.mouse.get_pos()
    cell_x, cell_y = coordinates_to_cell(*mouse_pos)
    # TODO: create more complicated check
    if (cell_x, cell_y) == prev_cell:
        # print('equal')
        return
    if field_matrix[cell_x][cell_y] != 0:
        return
    print('mouse move:', cell_x, cell_y)
    prev_cell = (cell_x, cell_y)
    change_cell(cell_x, cell_y, 1)


def start_drag():
    global drag, prev_cell
    drag = True
    mouse_pos = pygame.mouse.get_pos()
    cell_x, cell_y = coordinates_to_cell(*mouse_pos)
    prev_cell = cell_x, cell_y
    change_cell(cell_x, cell_y, 1)
    print('mouse down:', mouse_pos)


def stop_drag():
    global drag, prev_cell
    drag = False
    prev_cell = None
    mouse_pos = pygame.mouse.get_pos()
    print('mouse up:', mouse_pos)


def main():
    global field_matrix
    initialize_game_array()
    draw_grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_drag()
            elif event.type == pygame.MOUSEMOTION:
                mouse_move()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    stop_drag()


if __name__ == '__main__':
    main()
