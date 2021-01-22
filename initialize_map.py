import pygame


LIGHTGREY = (162, 162, 162)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (0, 177, 249)
NAVY = (1, 3, 142)
GREY = (128, 128, 128)
TURQUOISE = (1, 255, 247)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width  # keeps track of x,y coordinate
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def wall(self):
        return self.color == BLACK

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def start(self):
        self.color = NAVY

    def valid_point(self):
        self.color = LIGHTGREY

    def initialize_wall(self):
        self.color = BLACK

    def endpoint(self):
        self.color = TURQUOISE

    def path(self):
        self.color = LIGHTBLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].wall():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].wall():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].wall():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].wall():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False # function checks if the next square is valid or not