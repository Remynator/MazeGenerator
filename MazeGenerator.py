import time
import random
from ConfigFiles import Config as cfg


#  Make the initial cell the current_cell cell and mark it as visited
#  While there are unvisited cells
#       1.0 If the current_cell cell has any neighbours which have not been visited
#           1.1 Choose randomly one of the unvisited neighbours
#           1.2 Push the current_cell cell to the stack
#           1.3 Remove the walls between the current_cell cell and the next_cell cell
#           1.4 Make the next_cell cell the current_cell cell and mark it as visited
#       2.0 If the current_cell cell has any neighbours which have not been visited
#           2.1 Pop a cell fom the stack
#           2.2 Make it the current_cell cell


def remove_walls(cell_a, cell_b):
    x = cell_b.i - cell_a.i
    if x == -1:
        cell_a.walls[3] = False
        cell_b.walls[1] = False
    elif x == 1:
        cell_a.walls[1] = False
        cell_b.walls[3] = False

    y = cell_b.j - cell_a.j
    if y == -1:
        cell_a.walls[0] = False
        cell_b.walls[2] = False
    elif y == 1:
        cell_a.walls[2] = False
        cell_b.walls[0] = False


def setup_maze():
    cfg.canvas.delete("all")
    cfg.grid.clear()
    cfg.cells_visited.clear()
    cfg.cells_blocked.clear()

    for j in range(cfg.rows):
        for i in range(cfg.cols):
            cell = cfg.Cell(i, j, cfg.cell_size)
            cell.canvas = [None, None, None, None, None]

            cfg.grid.append(cell)

    cfg.cell_current = cfg.grid[cfg.index(random.randint(0, cfg.rows - 1), 0)]  # cfg.grid[cfg.index(0, 0)]
    cfg.cell_current.start = True
    cfg.cell_current.visited = True
    cfg.cells_visited.append(cfg.cell_current)

    rand_row = random.randint(0, cfg.rows - 1)  # cfg.rows - 1
    cell_end = cfg.grid[cfg.index(rand_row, cfg.cols - 1)]
    cell_end.end = True


def new_maze():
    from Menu.FileMenu import file_menu_close
    file_menu_close()

    setup_maze()
    stack = []

    while len(cfg.cells_visited) < cfg.rows * cfg.cols or len(stack) > 0:
        # STEP 1.1
        cell_next = cfg.cell_current.check_neighbors()

        if cell_next is not None:
            cell_next.visited = True
            cfg.cells_visited.append(cfg.cell_current)
            cfg.info_label.config(
                text=str(int(len(cfg.cells_visited) / (cfg.rows * cfg.cols / 1000)) / 10) + "% completed")
            # print(len(cfg.cells_visited) / (cfg.rows * cfg.cols / 100))

            # STEP 1.2
            stack.append(cfg.cell_current)

            # STEP 1.3
            remove_walls(cfg.cell_current, cell_next)

            # STEP 1.4
            cfg.cell_current.draw_cell()
            cfg.cell_current = cell_next
            cell_next.draw_cell()
        elif len(stack) > 0:
            # 2.1 # 2.2
            cfg.cell_current = stack.pop()

        time.sleep(0)

    cfg.gen_text = "Maze Generated: " + str(cfg.rows) + " R by " + str(cfg.cols) + " C, Cell size: " + str(
        cfg.cell_size)
    cfg.info_label.config(text=cfg.gen_text, justify="left")


def resize_maze():
    width = cfg.width_label.get()
    if width.isdigit():  # default 960  max 1776
        cfg.width = int(width)
    else:
        cfg.width = 960
        cfg.width_label.delete(0, len(cfg.width_label.get()))
        cfg.width_label.insert(0, cfg.width)

    cfg.root.update()

    height = cfg.height_label.get()
    if height.isdigit():  # default 480  max 1024
        cfg.height = int(height)
    else:
        cfg.height = 480
        cfg.height_label.delete(0, len(cfg.height_label.get()))
        cfg.height_label.insert(0, cfg.height)

    cell_size = cfg.cell_size_label.get()
    if cell_size.isdigit():  # default 16  min 16
        cfg.cell_size = int(cell_size)
    else:
        cfg.cell_size = 16
        cfg.cell_size_label.delete(0, len(cfg.cell_size_label.get()))
        cfg.cell_size_label.insert(0, cfg.cell_size)

    cfg.rows = int(cfg.height / cfg.cell_size)
    cfg.cols = int(cfg.width / cfg.cell_size)

    cfg.canvas.delete("all")
    cfg.canvas.config(width=cfg.width + cfg.border, height=cfg.height + cfg.border, bg="#cccccc")
