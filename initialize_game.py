import pygame
from queue import PriorityQueue
from initialize_map import Node
from initialize_map import GREY
from initialize_map import WHITE

ROWS = 40
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinder")


def distance_heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2  #
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    path_score = {spot: float("inf") for row in grid for spot in row}
    path_score[start] = 0

    pos_score = {spot: float("inf") for row in grid for spot in row}
    pos_score[start] = distance_heuristic(start.get_position(), end.get_position())  # heuristic estimates how far we
    # are from the end at the beginning

    node_set = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        node_set.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)  # makes the path
            end.endpoint()
            return True

        for neighbor in current.neighbors:
            tp_score = path_score[current] + 1

            if tp_score < path_score[neighbor]:  # if current tp_score is better than neighbor, then update the tp-score
                came_from[neighbor] = current
                path_score[neighbor] = tp_score
                pos_score[neighbor] = tp_score + distance_heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in node_set:
                    count += 1
                    open_set.put((pos_score[neighbor], count, neighbor))
                    # since neighbor has better path, update the final path
                    node_set.add(neighbor)
        draw()
        if current != start:
            current.valid_point()

    return False


def generate_board(rows, width):
    board = []
    gap = width // rows  # gives what the width of each cube should be
    for i in range(rows):
        board.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            board[i].append(spot)

    return board


def draw_on_board(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (GREY), (0, i * gap), (width, i * gap))  # draw horizontal lines
        for j in range(rows):
            pygame.draw.line(win, (GREY), (j * gap, 0), (j * gap, width))  # draw vertical lines


def draw(win, grid, rows, width):
    win.fill((WHITE))

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_on_board(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def controller(win, width):
    grid = generate_board(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.start()

                elif not end and spot != start:
                    end = spot
                    end.endpoint()

                elif spot != end and spot != start:
                    spot.initialize_wall()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = generate_board(ROWS, width)

    pygame.quit()


def main():
    controller(WINDOW, WIDTH)


if __name__ == '__main__':
    main()
