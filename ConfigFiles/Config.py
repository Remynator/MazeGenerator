import os
import math
import random
from tkinter import *


class Cell:

    def __init__(self, i, j, w):
        self.i = i
        self.j = j
        self.w = w
        self.visited = False
        self.start = False
        self.end = False
        self.blocked = False
        self.walls = [True, True, True, True]
        self.is_node = False
        self.index_node = None

    def __ini__(self):
        self.canvas = self.draw_cell()

    def draw_cell(self):
        x = self.i * self.w + border
        y = self.j * self.w + border
        draw = self.canvas
        canvas.delete(draw[0], draw[1], draw[2], draw[3], draw[4])

        if self.start:
            draw[0] = canvas.create_rectangle(x, y, x + self.w, y + self.w, fill="#00ff00", outline="")
        elif self.end:
            draw[0] = canvas.create_rectangle(x, y, x + self.w, y + self.w, fill="#ff0000", outline="")
        elif self.blocked:
            draw[0] = canvas.create_rectangle(x, y, x + self.w, y + self.w, fill="#000000", outline="")
        elif self.visited:
            draw[0] = canvas.create_rectangle(x, y, x + self.w, y + self.w, fill="#ffffff", outline="")

        if self.walls[0]:
            draw[1] = canvas.create_line(x, y, x + self.w, y, width=2)
        if self.walls[1]:
            draw[2] = canvas.create_line(x + self.w, y, x + self.w, y + self.w, width=2)
        if self.walls[2]:
            draw[3] = canvas.create_line(x, y + self.w, x + self.w, y + self.w, width=2)
        if self.walls[3]:
            draw[4] = canvas.create_line(x, y, x, y + self.w, width=2)

        root.update()
        return draw

    def check_neighbors(self):
        neighbors = []
        i = self.i
        j = self.j

        top =    grid[index(j - 1, i    )] if j > 0        else None
        right =  grid[index(j    , i + 1)] if i < cols - 1 else None
        bottom = grid[index(j + 1, i    )] if j < rows - 1 else None
        left =   grid[index(j    , i - 1)] if i > 0        else None

        if top and not top.visited and not top.blocked:
            neighbors.append(top)
        if right and not right.visited and not right.blocked:
            neighbors.append(right)
        if bottom and not bottom.visited and not bottom.blocked:
            neighbors.append(bottom)
        if left and not left.visited and not left.blocked:
            neighbors.append(left)

        if len(neighbors) > 0:
            r = random.randint(0, len(neighbors) - 1)
            return neighbors[r]
        else:
            return None


class Node:
    def __init__(self, i, j, w):
        self.i = i
        self.j = j
        self.w = w
        self.start = False
        self.end = False
        self.index = 0
        self.in_open = False
        self.in_closed = False
        self.is_path = False
        self.f = math.inf  # the cost of the path from the start to end
        self.g = math.inf  # the cost of the path from the start to node
        self.h = math.inf  # the cost of the path from the node to end
        self.connect = [None, None, None, None]
        self.parent = None

    def __int__(self):
        self.canvas = self.draw_node(False, False)

    def draw_node(self, draw_tf, draw_text_tf):
        x = self.i * self.w + border
        y = self.j * self.w + border
        draw = self.canvas
        canvas.delete(draw[0], draw[1], draw[2], draw[3])

        if self.is_path:
            color = "#0000ff"
            draw[1] = canvas.create_text(x + self.w / 6, y + self.w / 10, text=str(self.g))
            draw[2] = canvas.create_text(x + 5 * self.w / 6, y + self.w / 10, text=str(self.h))
            draw[3] = canvas.create_text(x + self.w / 2 - len("0"), y + 9 * self.w / 10, text=str(self.f))
        elif self.in_open:
            color = "#00ff00"
            draw[1] = canvas.create_text(x + self.w / 6, y + self.w / 10, text=str(self.g))
            draw[2] = canvas.create_text(x + 5 * self.w / 6, y + self.w / 10, text=str(self.h))
            draw[3] = canvas.create_text(x + self.w / 2 - len("0"), y + 9 * self.w / 10, text=str(self.f))
        elif self.in_closed:
            color = "#ff0000"
            draw[1] = canvas.create_text(x + self.w / 6, y + self.w / 10, text=str(self.g))
            draw[2] = canvas.create_text(x + 5 * self.w / 6, y + self.w / 10, text=str(self.h))
            draw[3] = canvas.create_text(x + self.w / 2 - len("0"), y + 9 * self.w / 10, text=str(self.f))
        else:
            color = "#ff00ff"

        if draw_tf == 1:
            draw[0] = canvas.create_oval(x + self.w / 4, y + self.w / 4, x + self.w * 3 / 4,
                                         y + self.w * 3 / 4, fill=color, outline="")
        if draw_text_tf == 0:
            canvas.delete(draw[1], draw[2], draw[3])

        root.update()
        return draw

    def connect_nodes(self):
        global cell_size
        x = self.i * self.w + border
        y = self.j * self.w + border
        cell_size = self.w
        draw = self.canvas
        canvas.delete(draw[4], draw[5], draw[6], draw[7])

        if self.connect[1] is not None and self.parent is None:
            next_node = self.connect[1]
            x_next = next_node.i * next_node.w + border
            y_next = next_node.j * next_node.w + border
            draw[4] = canvas.create_line(x + cell_size / 2, y + cell_size / 2, x_next + cell_size / 2,
                                         y_next + cell_size / 2, fill="#ff00ff")

        if self.connect[2] is not None and self.parent is None:
            next_node = self.connect[2]
            x_next = next_node.i * next_node.w + border
            y_next = next_node.j * next_node.w + border
            draw[5] = canvas.create_line(x + cell_size / 2, y + cell_size / 2, x_next + cell_size / 2,
                                         y_next + cell_size / 2, fill="#ff00ff")

        if self.parent is not None:
            next_node = self.parent
            x_next = next_node.i * next_node.w + border
            y_next = next_node.j * next_node.w + border
            draw[6] = canvas.create_line(x + cell_size / 2, y + cell_size / 2, x_next + cell_size / 2,
                                         y_next + cell_size / 2, fill="#00ffff", width=2)
            # canvas.create_text(x + cell_size / 2, y + cell_size / 2, text=index(next_node.j, next_node.i))

        if self.is_path:
            next_node = self.parent
            x_next = next_node.i * next_node.w + border
            y_next = next_node.j * next_node.w + border
            draw[7] = canvas.create_line(x + cell_size / 2, y + cell_size / 2, x_next + cell_size / 2,
                                         y_next + cell_size / 2, fill="#0000ff", width=2)

        root.update()
        return draw


root_dir = ""

root = Tk()
rows, cols, cell_size, border = 0, 0, 0, 0
width, height, grid = 0, 0, []
cell_current = None
cells_visited, cells_blocked = [], []
gen_text, save_text, load_text, solve_maze_text = "", "", "", ""

frame = Frame(root)
canvas = Canvas(frame)
info_label = Label(root)
width_label = Entry(root)
height_label = Entry(root)
cell_size_label = Entry(root)
status_bar = Label(root)

pause_entry = Entry(root)
save_var = IntVar()
movie_var = IntVar()
draw_nodes_var = IntVar()
draw_text_var = IntVar()
save_box = Checkbutton(root)


def init():
    global root_dir
    global width, height, cell_size, border
    global rows, cols, grid
    global cells_visited, cells_blocked
    global cell_current
    global gen_text, save_text, load_text, solve_maze_text

    width = 960
    height = 640
    cell_size = 64
    border = 4

    rows = int(height / cell_size)
    cols = int(width / cell_size)
    grid = []

    cell_current = None
    cells_visited = []
    cells_blocked = []

    gen_text = ""
    save_text = ""
    load_text = ""
    solve_maze_text = ""


def index(row, col):
    return row * cols + col
