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

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

# Global variables
global field_matrix

# State
drag = False
prev_prev_cell = None
prev_cell = None
cur_cell = None


# Field constants
class CELL_VALUES:
    class EMPTY:
        num = 0
        desc = 'empty'
        img = pygame.transform.scale(pygame.image.load('images/empty.png'), (CELL_SIZE, CELL_SIZE))
    class LEFT_UP:
        num = 1
        desc = 'left up'
        img = pygame.transform.scale(pygame.image.load('images/left up.png'), (CELL_SIZE, CELL_SIZE))
    class HORIZONTAL:
        num = 2
        desc = 'horizontal'
        img = pygame.transform.scale(pygame.image.load('images/horizontal.png'), (CELL_SIZE, CELL_SIZE))
    class RIGHT_UP:
        num = 3
        desc = 'right up'
        img = pygame.transform.scale(pygame.image.load('images/right up.png'), (CELL_SIZE, CELL_SIZE))
    class VERTICAL:
        num = 4
        desc = 'vertical'
        img = pygame.transform.scale(pygame.image.load('images/vertical.png'), (CELL_SIZE, CELL_SIZE))
    class LEFT_DOWN:
        num = 7
        desc = 'left down'
        img = pygame.transform.scale(pygame.image.load('images/left down.png'), (CELL_SIZE, CELL_SIZE))
    class RIGHT_DOWN:
        num = 9
        desc = 'right down'
        img = pygame.transform.scale(pygame.image.load('images/right down.png'), (CELL_SIZE, CELL_SIZE))

class QUARTER:
    UP = 2
    DOWN = 8
    LEFT = 4
    RIGHT = 6


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
    global field_matrix
    field_matrix = [[CELL_VALUES.EMPTY] * ROWS for _ in range(ROWS)]


def coordinates_to_cell(x, y):
    cell_x = x // CELL_SIZE
    cell_y = y // CELL_SIZE
    return cell_x, cell_y


def cell_quarter(x, y, cell_x, cell_y):
    x -= cell_x * CELL_SIZE
    y -= cell_y * CELL_SIZE
    if (y <= x) and (y <= CELL_SIZE - x):
        return QUARTER.UP
    elif (y <= x) and (y > CELL_SIZE - x):
        return QUARTER.RIGHT
    elif (y > x) and (y <= CELL_SIZE - x):
        return QUARTER.LEFT
    elif (y > x) and (y > CELL_SIZE - x):
        return QUARTER.DOWN


def neighbor_by_quarter(cell_x, cell_y, quarter):
    if quarter == QUARTER.UP:
        return cell_x, cell_y - 1
    elif quarter == QUARTER.LEFT:
        return cell_x - 1, cell_y
    elif quarter == QUARTER.RIGHT:
        return cell_x + 1, cell_y
    elif quarter == QUARTER.DOWN:
        return cell_x, cell_y + 1


def cell_image_coordinates(cell_x, cell_y):
    x = CELL_SIZE * cell_x
    y = CELL_SIZE * cell_y
    return x, y


def fill_cell(cell_x, cell_y):
    x, y = cell_image_coordinates(cell_x, cell_y)
    value = field_matrix[cell_x][cell_y]
    # TODO: May be done better
    window.blit(CELL_VALUES.EMPTY.img, (x, y))
    window.blit(value.img, (x, y))
    pygame.display.update()


def change_cell(cell_x, cell_y, value):
    # TODO: add case value ?
    field_matrix[cell_x][cell_y] = value
    fill_cell(cell_x, cell_y)


def calculate_cell_values(prev_cell, cur_cell, next_cell):
    print(prev_cell, cur_cell, next_cell)
    cell_matrix = {
        (None, None): CELL_VALUES.HORIZONTAL,  # impossible
        (None, (-1, 0)): CELL_VALUES.HORIZONTAL,
        (None, (1, 0)): CELL_VALUES.HORIZONTAL,
        (None, (0, -1)): CELL_VALUES.VERTICAL,
        (None, (0, 1)): CELL_VALUES.VERTICAL,
        ((-1, 0), (1, 0)): CELL_VALUES.HORIZONTAL,
        ((-1, 0), (0, -1)): CELL_VALUES.LEFT_UP,
        ((-1, 0), (0, 1)): CELL_VALUES.LEFT_DOWN,
        # ((1, 0), (-1, 0))
        ((0, -1), (1, 0)): CELL_VALUES.RIGHT_UP,
        ((0, 1), (1, 0)): CELL_VALUES.RIGHT_DOWN,
        ((0, -1), (0, 1)): CELL_VALUES.VERTICAL,
        # ((0, -1), (-1, 0))
        # ((0, -1), (1, 0))
        # ((0, 1), (0, -1))
        # ((0, 1), (-1, 0))
        # ((0, 1), (1, 0))
    }

    if prev_cell is not None:
        first = (prev_cell[0] - cur_cell[0], prev_cell[1] - cur_cell[1])
    else:
        first = None

    if cur_cell is not None:
        second = (next_cell[0] - cur_cell[0], next_cell[1] - cur_cell[1])
    else:
        second = None

    if first is None:
        return cell_matrix[(first, second)]
    # print(first, second)
    # print((first, second))
    # print(sorted((first, second)))
    return cell_matrix[tuple(sorted((first, second)))]


'''Main logic:
If current cell isn't empty, ignore it
Let's create condition, if cur_cell changed

Cases:
+ Start from not empty cell - just ignore it
+ Mouse moves on not empty cell - finish pipe
+ Drag ends on not empty cell - prev will fix it
+ From start move to prohibited cell - finish pipe

Good logic:
Store all the pipe route as an object, that we can cancel or smth (move, rotate)
'''


def mouse_move():
    global prev_prev_cell, prev_cell
    if not drag:
        return
    mouse_pos = pygame.mouse.get_pos()
    cell_x, cell_y = coordinates_to_cell(*mouse_pos)
    # print(cell_quarter(*mouse_pos, cell_x, cell_y))

    if (cell_x, cell_y) == prev_cell:
        return
    if field_matrix[cell_x][cell_y] != CELL_VALUES.EMPTY:
        stop_drag()
        return
    if (cell_x, cell_y) == prev_prev_cell:
        stop_drag()
        return
    print('mouse move:', cell_x, cell_y)
    value = calculate_cell_values(prev_prev_cell, prev_cell, (cell_x, cell_y))
    change_cell(*prev_cell, value)

    quarter = cell_quarter(*mouse_pos, cell_x, cell_y)
    next_cell = neighbor_by_quarter(cell_x, cell_y, quarter)
    if next_cell == prev_cell:
        next_cell = None
    # Smth like a hack - using function backwards
    value = calculate_cell_values(next_cell, (cell_x, cell_y), prev_cell)
    change_cell(cell_x, cell_y, value)
    # TODO: Logical error - prev_cell becomes current cell too early
    prev_prev_cell = prev_cell
    prev_cell = (cell_x, cell_y)


def start_drag():
    global drag, prev_prev_cell, prev_cell, cur_cell
    mouse_pos = pygame.mouse.get_pos()
    print('mouse down:', mouse_pos)
    cur_cell = coordinates_to_cell(*mouse_pos)
    cell_x, cell_y = cur_cell
    if field_matrix[cell_x][cell_y] != CELL_VALUES.EMPTY:
        return
    drag = True
    quarter = cell_quarter(*mouse_pos, cell_x, cell_y)
    prev_prev_cell = neighbor_by_quarter(cell_x, cell_y, quarter)
    prev_cell = (cell_x, cell_y)
    value = calculate_cell_values(None, (cell_x, cell_y), prev_prev_cell)
    change_cell(cell_x, cell_y, value)


def stop_drag():
    global drag, prev_prev_cell, prev_cell
    if not drag:
        return
    mouse_pos = pygame.mouse.get_pos()
    print('mouse up:', mouse_pos)
    cur_cell = coordinates_to_cell(*mouse_pos)
    cell_x, cell_y = cur_cell
    if cur_cell != prev_cell:
        if prev_prev_cell == cur_cell:
            prev_prev_cell = None
        value = calculate_cell_values(prev_prev_cell, prev_cell, cur_cell)
        change_cell(*prev_cell, value)
    else:
        quarter = cell_quarter(*mouse_pos, cell_x, cell_y)
        next_cell = neighbor_by_quarter(cell_x, cell_y, quarter)
        if next_cell == prev_prev_cell:
            next_cell = None
        value = calculate_cell_values(next_cell, cur_cell, prev_prev_cell)
        change_cell(cell_x, cell_y, value)
    drag = False
    prev_prev_cell = None
    prev_cell = None


def main():
    global field_matrix
    initialize_game_array()
    draw_grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                # pygame.quit()
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
