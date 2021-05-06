import pygame
from copy import deepcopy

# Colors
from pipe import Pipe

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Field constants
# class CELL_VALUES:
#     def __init__(self, cell_size):
#         self.cell_size = cell_size
#
#     class RESERVED:
#         num = -1
#         desc = 'reserved'
#         img = pygame.transform.scale(pygame.image.load('images/empty.png'), (self.cell_size, self.cell_size))
#
#     class EMPTY:
#         num = 0
#         desc = 'empty'
#         img = pygame.transform.scale(pygame.image.load('images/empty.png'), (self.cell_size, self.cell_size))
#
#     class LEFT_UP:
#         num = 1
#         desc = 'left up'
#         img = pygame.transform.scale(pygame.image.load('images/left up.png'), (self.cell_size, self.cell_size))
#
#     class HORIZONTAL:
#         num = 2
#         desc = 'horizontal'
#         img = pygame.transform.scale(pygame.image.load('images/horizontal.png'), (self.cell_size, self.cell_size))
#
#     class RIGHT_UP:
#         num = 3
#         desc = 'right up'
#         img = pygame.transform.scale(pygame.image.load('images/right up.png'), (self.cell_size, self.cell_size))
#
#     class VERTICAL:
#         num = 4
#         desc = 'vertical'
#         img = pygame.transform.scale(pygame.image.load('images/vertical.png'), (self.cell_size, self.cell_size))
#
#     class LEFT_DOWN:
#         num = 7
#         desc = 'left down'
#         img = pygame.transform.scale(pygame.image.load('images/left down.png'), (self.cell_size, self.cell_size))
#
#     class RIGHT_DOWN:
#         num = 9
#         desc = 'right down'
#         img = pygame.transform.scale(pygame.image.load('images/right down.png'), (self.cell_size, self.cell_size))

class CELL_VALUES:
    RESERVED = -1
    EMPTY = 0
    LEFT_UP = 1
    HORIZONTAL = 2
    RIGHT_UP = 3
    VERTICAL = 4
    LEFT_DOWN = 7
    RIGHT_DOWN = 9


# def get_cell_values(cell_size):
#     return {
#         'RESERVED': {
#             'num': -1,
#             'desc': 'reserved',
#             'img': pygame.transform.scale(pygame.image.load('images/empty.png'), (cell_size, cell_size)),
#         },
#         'EMPTY': {
#             'num': 0,
#             'desc': 'empty',
#             'img': pygame.transform.scale(pygame.image.load('images/empty.png'), (cell_size, cell_size)),
#         },
#         'LEFT_UP': {
#             'num': 1,
#             'desc': 'left up',
#             'img': pygame.transform.scale(pygame.image.load('images/left up.png'), (cell_size, cell_size)),
#         },
#         'HORIZONTAL': {
#             'num': 2,
#             'desc': 'horizontal',
#             'img': pygame.transform.scale(pygame.image.load('images/horizontal.png'), (cell_size, cell_size)),
#         },
#         'RIGHT_UP': {
#             'num': 3,
#             'desc': 'right up',
#             'img': pygame.transform.scale(pygame.image.load('images/right up.png'), (cell_size, cell_size)),
#         },
#         'VERTICAL': {
#             'num': 4,
#             'desc': 'vertical',
#             'img': pygame.transform.scale(pygame.image.load('images/vertical.png'), (cell_size, cell_size)),
#         },
#         'LEFT_DOWN': {
#             'num': 7,
#             'desc': 'left down',
#             'img': pygame.transform.scale(pygame.image.load('images/left down.png'), (cell_size, cell_size)),
#         },
#         'RIGHT_DOWN': {
#             'num': 9,
#             'desc': 'right down',
#             'img': pygame.transform.scale(pygame.image.load('images/right down.png'), (cell_size, cell_size)),
#         },
#     }


def get_cell_values_images(cell_size):
    return {
        CELL_VALUES.RESERVED:
            pygame.transform.scale(pygame.image.load('images/reserved_gray.png'), (cell_size, cell_size)),
        CELL_VALUES.EMPTY:
            pygame.transform.scale(pygame.image.load('images/empty_gray.png'), (cell_size, cell_size)),
        CELL_VALUES.LEFT_UP:
            pygame.transform.scale(pygame.image.load('images/left up.png'), (cell_size, cell_size)),
        CELL_VALUES.HORIZONTAL:
            pygame.transform.scale(pygame.image.load('images/horizontal.png'), (cell_size, cell_size)),
        CELL_VALUES.RIGHT_UP:
            pygame.transform.scale(pygame.image.load('images/right up.png'), (cell_size, cell_size)),
        CELL_VALUES.VERTICAL:
            pygame.transform.scale(pygame.image.load('images/vertical.png'), (cell_size, cell_size)),
        CELL_VALUES.LEFT_DOWN:
            pygame.transform.scale(pygame.image.load('images/left down.png'), (cell_size, cell_size)),
        CELL_VALUES.RIGHT_DOWN:
            pygame.transform.scale(pygame.image.load('images/right down.png'), (cell_size, cell_size)),
    }


class QUARTER:
    UP = 2
    DOWN = 8
    LEFT = 4
    RIGHT = 6


class Game:
    def __init__(self, window_size, rows):
        self.window_size = window_size
        self.rows = rows
        self.cell_size = self.window_size // self.rows
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        # self.CELL_VALUES = get_cell_values(self.cell_size)
        self.CELL_VALUES_IMAGES = get_cell_values_images(self.cell_size)

        self.field = [[CELL_VALUES.EMPTY] * self.rows for _ in range(self.rows)]
        self.prev_field = deepcopy(self.field)

        self.cur_cell = None
        self.cur_quarter = None
        self.pipe_drag = False
        self.pipe_path = None
        self.ball_drag = False

    def init_pipe_parameters(self):
        self.cur_cell = None
        self.cur_quarter = None
        self.pipe_drag = False
        self.pipe_path = None

    def draw_grid(self):
        """Fill field white and draw cells"""
        # Starting points
        x = 0
        y = 0

        self.window.fill(WHITE)
        for i in range(self.rows):
            x = i * self.cell_size
            pygame.draw.line(self.window, GRAY, (x, 0), (x, self.window_size), 3)
            pygame.draw.line(self.window, GRAY, (0, x), (self.window_size, x), 3)

        pygame.display.update()

    def start(self):
        pygame.init()
        pygame.display.set_caption("Pipes")

        # self.draw_grid()
        self.draw_field()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                    # pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.start_draw_pipe()
                elif event.type == pygame.MOUSEMOTION:
                    self.continue_draw_pipe()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.stop_draw_pipe()

    def coordinates_to_cell(self, x, y):
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        return cell_x, cell_y

    def get_cur_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        cur_cell = self.coordinates_to_cell(*mouse_pos)
        return cur_cell

    def draw_field(self):
        # print('Redraw field')
        for x in range(len(self.field)):
            for y in range(len(self.field[x])):
                self.fill_cell(x, y)

    def cancel_pipe(self):
        """"""
        self.field = deepcopy(self.prev_field)
        self.draw_field()
        self.init_pipe_parameters()

    def cell_image_coordinates(self, cell_x, cell_y):
        x = self.cell_size * cell_x
        y = self.cell_size * cell_y
        return x, y

    def fill_cell(self, cell_x, cell_y):
        x, y = self.cell_image_coordinates(cell_x, cell_y)
        value = self.field[cell_x][cell_y]
        # TODO: May be done better
        self.window.blit(self.CELL_VALUES_IMAGES[CELL_VALUES.EMPTY], (x, y))
        self.window.blit(self.CELL_VALUES_IMAGES[value], (x, y))
        pygame.display.update()

    def change_cell(self, cell_x, cell_y, value):
        self.field[cell_x][cell_y] = value
        self.fill_cell(cell_x, cell_y)

    def get_cell_quarter(self, x, y, cell_x, cell_y):
        x -= cell_x * self.cell_size
        y -= cell_y * self.cell_size
        if (y <= x) and (y <= self.cell_size - x):
            return QUARTER.UP
        elif (y <= x) and (y > self.cell_size - x):
            return QUARTER.RIGHT
        elif (y > x) and (y <= self.cell_size - x):
            return QUARTER.LEFT
        elif (y > x) and (y > self.cell_size - x):
            return QUARTER.DOWN

    def neighbor_by_quarter(self, cell_x, cell_y, quarter):
        if quarter == QUARTER.UP:
            return cell_x, cell_y - 1
        elif quarter == QUARTER.LEFT:
            return cell_x - 1, cell_y
        elif quarter == QUARTER.RIGHT:
            return cell_x + 1, cell_y
        elif quarter == QUARTER.DOWN:
            return cell_x, cell_y + 1

    def get_neighbor_by_quarter(self):
        x, y = pygame.mouse.get_pos()
        quarter = self.get_cell_quarter(x, y, *self.cur_cell)
        neighbor = self.neighbor_by_quarter(*self.cur_cell, quarter)
        return neighbor

    def cell_changed(self):
        return self.cur_cell != self.get_cur_cell()

    def quarter_changed(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.cur_quarter != self.get_cell_quarter(*mouse_pos, *self.cur_cell)

    def calculate_cell_value(self, prev_cell, cur_cell, next_cell):
        # print(prev_cell, cur_cell, next_cell)
        if prev_cell == next_cell:
            prev_cell = None
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

    def get_finish_cell(self):
        next_cell = self.get_neighbor_by_quarter()
        prev_cell = self.pipe_path[-1]
        if next_cell == prev_cell:
            prev_x, prev_y = prev_cell
            cur_x, cur_y = self.cur_cell
            next_x = cur_x + (cur_x - prev_x)
            next_y = cur_y + (cur_y - prev_y)
            next_cell = next_x, next_y
        return next_cell

    def start_draw_pipe(self):
        self.cur_cell = self.get_cur_cell()
        # TODO: How to do without this vars
        cell_x, cell_y = self.cur_cell
        if self.field[cell_x][cell_y] != CELL_VALUES.EMPTY:
            return
        mouse_pos = pygame.mouse.get_pos()
        self.cur_quarter = self.get_cell_quarter(*mouse_pos, *self.cur_cell)
        prev_cell = self.get_neighbor_by_quarter()
        prev_cell_x, prev_cell_y = prev_cell
        if self.field[prev_cell_x][prev_cell_y] not in [CELL_VALUES.EMPTY, CELL_VALUES.RESERVED]:
            return

        self.pipe_drag = True
        self.prev_field = deepcopy(self.field)
        self.pipe_path = [prev_cell]
        self.change_cell(*prev_cell, CELL_VALUES.RESERVED)
        value = self.calculate_cell_value(None, self.cur_cell, prev_cell)
        self.change_cell(*self.cur_cell, value)

    def continue_draw_pipe(self):
        if not self.pipe_drag:
            return

        '''Main logic
        + Store only cur_cell and path
        + Check, if cell changed
        + On change check is change correct (empty or reserved cell)
        + If not correct - cancel pipe (remove all values from path - carefully)
            Maybe - stop, if it's easier to do
        + If correct - update cur_cell and path
        + If len(path) > 2 - draw smth
        '''

        # print('path:', self.pipe_path)
        if not self.cell_changed():
            if not self.quarter_changed():
                return
            mouse_pos = pygame.mouse.get_pos()
            self.cur_quarter = self.get_cell_quarter(*mouse_pos, *self.cur_cell)
            next_cell = self.get_neighbor_by_quarter()
            prev_cell = self.pipe_path[-1]
            value = self.calculate_cell_value(prev_cell, self.cur_cell, next_cell)
            self.change_cell(*self.cur_cell, value)
            return

        cur_cell = self.get_cur_cell()
        cur_x, cur_y = cur_cell
        if self.field[cur_x][cur_y] != CELL_VALUES.EMPTY:
            self.cancel_pipe()
            return

        prev_cell = self.cur_cell
        self.cur_cell = cur_cell
        self.pipe_path.append(prev_cell)
        value = self.calculate_cell_value(None, self.cur_cell, prev_cell)
        self.change_cell(*self.cur_cell, value)

    def stop_draw_pipe(self):
        if not self.pipe_drag:
            return
        # add cur and next cells to the path
        next_cell = self.get_finish_cell()
        next_x, next_y = next_cell
        # If next cell not in [empty, reserved] - cancel pipe
        if self.field[next_x][next_y] not in [CELL_VALUES.EMPTY, CELL_VALUES.RESERVED]:
            self.cancel_pipe()
            return
        self.pipe_path += [self.cur_cell, next_cell]
        # make next cell reserved
        self.change_cell(*next_cell, CELL_VALUES.RESERVED)
        Pipe(self.pipe_path)
        self.init_pipe_parameters()