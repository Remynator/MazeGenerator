from tkinter import *
import PathFinder.PathFinder as PathFinder
import PathFinder.HelperFile as HelperFile
import pandas as pd
import os
import sys
import time
import datetime
import math
import random


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


class Cell:

    def __int__(self, i, j, w):
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
        self.canvas = self.draw_cell()

    def draw_cell(self):
        global cell_size
        x = self.i * self.w + border
        y = self.j * self.w + border
        cell_size = self.w
        draw = self.canvas
        canvas.delete(draw[0], draw[1], draw[2], draw[3], draw[4])

        if self.start:
            draw[0] = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="#00ff00", outline="")
        elif self.end:
            draw[0] = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="#ff0000", outline="")
        elif self.blocked:
            draw[0] = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="#000000", outline="")
        elif self.visited:
            draw[0] = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="#ffffff", outline="")

        if self.walls[0]:
            draw[1] = canvas.create_line(x, y, x + cell_size, y, width=2)
        if self.walls[1]:
            draw[2] = canvas.create_line(x + cell_size, y, x + cell_size, y + cell_size, width=2)
        if self.walls[2]:
            draw[3] = canvas.create_line(x, y + cell_size, x + cell_size, y + cell_size, width=2)
        if self.walls[3]:
            draw[4] = canvas.create_line(x, y, x, y + cell_size, width=2)

        # root.update()
        return draw

    def check_neighbors(self):
        neighbors = []
        i = self.i
        j = self.j

        top = None
        right = None
        bottom = None
        left = None

        if j > 0:
            top = grid[index(j - 1, i)]
        if i < cols - 1:
            right = grid[index(j, i + 1)]
        if j < rows - 1:
            bottom = grid[index(j + 1, i)]
        if i > 0:
            left = grid[index(j, i - 1)]

        if top is not None and not top.visited and not top.blocked:
            neighbors.append(top)
        if right is not None and not right.visited and not right.blocked:
            neighbors.append(right)
        if bottom is not None and not bottom.visited and not bottom.blocked:
            neighbors.append(bottom)
        if left is not None and not left.visited and not left.blocked:
            neighbors.append(left)

        if len(neighbors) > 0:
            r = random.randint(0, len(neighbors) - 1)
            return neighbors[r]
        else:
            return None


class Node:
    def __int__(self, i, j, w):
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
        self.connect = [Node(), Node(), Node(), Node()]
        self.parent = Node()
        self.canvas = self.draw_node(False, False)

    def draw_node(self, draw_tf, draw_text_tf):
        global cell_size
        x = self.i * self.w + border
        y = self.j * self.w + border
        cell_size = self.w
        draw = self.canvas
        canvas.delete(draw[0], draw[1], draw[2], draw[3])

        if self.is_path:
            color = "#0000ff"
            draw[1] = canvas.create_text(x + cell_size / 6, y + cell_size / 10, text=str(self.g))
            draw[2] = canvas.create_text(x + 5 * cell_size / 6, y + cell_size / 10, text=str(self.h))
            draw[3] = canvas.create_text(x + cell_size / 2 - len("0"), y + 9 * cell_size / 10, text=str(self.f))
        elif self.in_open:
            color = "#00ff00"
            draw[1] = canvas.create_text(x + cell_size / 6, y + cell_size / 10, text=str(self.g))
            draw[2] = canvas.create_text(x + 5 * cell_size / 6, y + cell_size / 10, text=str(self.h))
            draw[3] = canvas.create_text(x + cell_size / 2 - len("0"), y + 9 * cell_size / 10, text=str(self.f))
        elif self.in_closed:
            color = "#ff0000"
            draw[1] = canvas.create_text(x + cell_size / 6, y + cell_size / 10, text=str(self.g))
            draw[2] = canvas.create_text(x + 5 * cell_size / 6, y + cell_size / 10, text=str(self.h))
            draw[3] = canvas.create_text(x + cell_size / 2 - len("0"), y + 9 * cell_size / 10, text=str(self.f))
        else:
            color = "#ff00ff"

        if draw_tf == 1:
            draw[0] = canvas.create_oval(x + cell_size / 4, y + cell_size / 4, x + cell_size * 3 / 4,
                                         y + cell_size * 3 / 4, fill=color, outline="")
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


def close_window():
    root.destroy()


def index(i, j):
    return i * cols + j


def setup_maze():
    global cell_current

    canvas.delete("all")
    grid.clear()
    cells_visited.clear()
    cells_blocked.clear()

    for j in range(rows):
        for i in range(cols):
            cell = Cell()
            cell.i = i
            cell.j = j
            cell.w = cell_size
            cell.start = False
            cell.end = False
            cell.blocked = False
            cell.visited = False
            cell.walls = [True, True, True, True]
            cell.is_node = False
            cell.index_node = None
            cell.canvas = [None, None, None, None, None]

            grid.append(cell)

    cell_current = grid[index(0, 0)]  # grid[index(random.randint(0, rows - 1), 0)]
    cell_current.start = True
    cell_current.visited = True
    cells_visited.append(cell_current)

    rand_row = rows - 1  # random.randint(0, rows - 1)
    cell_end = grid[index(rand_row, cols - 1)]
    cell_end.end = True
    radius = math.ceil(cols * .1) if math.ceil(cols * .1) <= 4 else 4

    for k in range(-radius, 1):
        m = -radius - k
        while m <= radius + k:
            if 0 <= (rand_row + m) < rows:
                blocked_cell = grid[index(rand_row + m, cols - 1 + k)]
                blocked_cell.blocked = False
                cells_blocked.append(blocked_cell)
            m += 1


def generate_maze():
    setup_maze()
    global gen_text, save_text, load_text, solve_maze_text
    global cell_current
    global cell_next

    while len(cells_visited) < rows * cols or len(stack) > 0:
        # STEP 1.1
        cell_next = cell_current.check_neighbors()

        if cell_next is not None:
            cell_next.visited = True
            cells_visited.append(cell_current)
            done_label.config(text=str(int(len(cells_visited) / (rows * cols / 1000)) / 10) + "% completed")
            # print(len(cells_visited) / (rows * cols / 100))
            if len(cells_visited) > rows * cols * .75:
                for m in range(len(cells_blocked)):
                    cells_blocked[m].blocked = False

            # STEP 1.2
            stack.append(cell_current)

            # STEP 1.3
            HelperFile.remove_walls(cell_current, cell_next)

            # STEP 1.4
            cell_current.draw_cell()
            cell_current = cell_next
            cell_next.draw_cell()
        elif len(stack) > 0:
            # 2.1 # 2.2
            cell_current = stack.pop()

        time.sleep(0)

    file_name_label.delete(0, len(file_name_label.get()))
    file_name_label.insert(0, str(datetime.datetime.now().strftime("%Y-%m-%d_%H;%M")))

    gen_text = "Maze Generated: " + str(rows) + " R by " + str(cols) + " C, Cell size: " + str(cell_size)
    done_label.config(text=gen_text, justify="left")


def resize_maze():
    global cell_size
    global rows
    global cols
    global grid
    global border

    new_width = width_label.get()
    if new_width.isdigit():  # default 960  max 1776
        new_width = int(new_width)
    else:
        new_width = 960
        width_label.delete(0, len(width_label.get()))
        width_label.insert(0, new_width)

    new_height = height_label.get()
    if new_height.isdigit():  # default 480  max 1024
        new_height = int(new_height)

    else:
        new_height = 480
        height_label.delete(0, len(height_label.get()))
        height_label.insert(0, new_height)

    cell_size = cell_size_label.get()
    if cell_size.isdigit():  # default 16  min 16
        cell_size = int(cell_size)
    else:
        cell_size = 16
        cell_size_label.delete(0, len(cell_size_label.get()))
        cell_size_label.insert(0, cell_size)

    rows = int(new_height / cell_size)
    cols = int(new_width / cell_size)

    canvas.delete("all")
    canvas.config(width=new_width + border, height=new_height + border, bg="#cccccc")


def save_to_csv():
    global gen_text, save_text, load_text, solve_maze_text
    folder_name = file_name_label.get()
    folder_path = os.path.join(ROOT_DIR, "Mazes", folder_name)
    file_name = folder_name + ".csv"
    file_path = os.path.join(folder_path, file_name)

    if save_var.get() == 1:
        try:
            pd.read_csv(file_path)
        except FileNotFoundError:
            HelperFile.create_new_folder(folder_path)

            f = open(file_path, "w+")
            f.write("col_nr,row_nr,cell_size,visited,blocked,start,end,wall_top,wall_right,wall_bottom,wall_left\n")

            for i in range(len(grid)):
                write_cell = grid[i]
                f.write(str(write_cell.i) + "," + str(write_cell.j) + "," + str(write_cell.w) + "," + str(
                    write_cell.visited) + "," + str(write_cell.blocked) + "," + str(write_cell.start) + "," + str(
                    write_cell.end) + "," + str(write_cell.walls[0]) + "," + str(write_cell.walls[1]) + "," + str(
                    write_cell.walls[2]) + "," + str(write_cell.walls[3]) + "\n")

            f.close()
            save_text = "\nMaze Saved as: " + file_name
            done_label.config(text=gen_text + save_text, justify="left")

    return folder_name, folder_path


def load_maze():
    global gen_text, save_text, load_text, solve_maze_text
    try:
        folder_name = file_name_label.get()
        file_name = folder_name + ".csv"
        file_path = os.path.join(ROOT_DIR, "Mazes", folder_name, file_name)

        df = pd.read_csv(file_path)
        array = df.to_numpy()
        cell_list = []

        for i in range(len(array)):
            # col_nr, row_nr, visited, cell_size, blocked, start, end, wall_top, wall_right, wall_bottom, wall_left
            cell = Cell()
            cell.i = array[i][0]
            cell.j = array[i][1]
            cell.w = array[i][2]
            cell.visited = array[i][3]
            cell.blocked = array[i][4]
            cell.start = array[i][5]
            cell.end = array[i][6]
            walls = []
            for j in range(4):
                walls.append(array[i][7 + j])
            cell.walls = walls

            cell.is_node = False
            cell.index_node = None
            cell.canvas = [None, None, None, None, None]

            cell_list.append(cell)

    except FileNotFoundError:
        if len(grid) > 1:
            cell_list = grid
        else:
            sys.exit('No Cells')

    canvas.delete("all")
    draw_all_cells(cell_list)

    last_cell = cell_list[len(cell_list) - 1]
    new_width = (last_cell.i + 1) * last_cell.w
    new_height = (last_cell.j + 1) * last_cell.w

    canvas.config(width=new_width + border, height=new_height + border, bg="#cccccc")

    cell_nodes = find_nodes(cell_list)
    node_list = connect_nodes(cell_nodes[0], cell_nodes[1])

    gen_text = "Maze Generated: " + str(rows) + " R by " + str(cols) + " C, Cell size: " + str(cell_size)
    load_text = "\nMaze Loaded: " + str(len(node_list)) + "/" + str(rows * cols) + " Nodes"
    done_label.config(text=gen_text + save_text + load_text, justify="left")
    root.update()
    return node_list


def draw_all_cells(cell_list):
    for i in range(len(cell_list)):
        cell = cell_list[i]
        cell.draw_cell()


def find_nodes(cell_list):
    global rows, cols
    nodes_list = []

    for i in range(len(cell_list)):
        cell = cell_list[i]

        if not cell.walls[0] == cell.walls[2] or not cell.walls[1] == cell.walls[3] or cell.start or cell.end or (
                cell.walls[0] == cell.walls[1] and cell.walls[0] == cell.walls[2] and cell.walls[0] == cell.walls[3]):
            cell.is_node = True
            cell.index_node = len(nodes_list)

            node = Node()
            node.i = cell.i
            node.j = cell.j
            node.w = cell.w
            node.start = cell.start
            node.end = cell.end
            node.index = len(nodes_list)
            node.is_path = False
            node.in_open = False
            node.in_closed = False
            node.f = math.inf
            node.g = math.inf
            node.h = math.inf
            node.connect = [None, None, None, None]
            node.parent = None
            node.canvas = [None, None, None, None, None, None, None, None]
            nodes_list.append(node)

            # node.draw_node(draw_nodes_var.get(), draw_text_var.get())
        else:
            cell.is_node = False
            cell.index_node = None

    last_cell = cell_list[len(cell_list) - 1]
    rows = last_cell.j + 1
    cols = last_cell.i + 1

    return cell_list, nodes_list


def connect_nodes(cell_list, nodes_list):
    global rows, cols
    last_cell = cell_list[len(cell_list) - 1]
    rows = int(last_cell.j + 1)
    cols = int(last_cell.i + 1)

    for i in range(len(nodes_list)):
        start_node = nodes_list[i]
        start_cell = cell_list[index(start_node.j, start_node.i)]

        if not start_cell.walls[1]:
            for j in range(start_cell.i + 1, cols):
                check_cell = cell_list[index(start_cell.j, j)]

                if check_cell.is_node:
                    check_node = nodes_list[check_cell.index_node]
                    start_node.connect[1] = check_node
                    check_node.connect[3] = start_node
                    break

        if not start_cell.walls[2]:
            for j in range(start_cell.j + 1, rows):
                check_cell = cell_list[index(j, start_cell.i)]

                if check_cell.is_node:
                    check_node = nodes_list[check_cell.index_node]
                    start_node.connect[2] = check_node
                    check_node.connect[0] = start_node
                    break

        # start_node.connect_nodes()
        # start_node.draw_node(draw_nodes_var.get(), draw_text_var.get())

    return nodes_list


def solve_maze():
    global gen_text, save_text, load_text, solve_maze_text
    folder = save_to_csv()
    file_path = os.path.join(folder[1], folder[0])

    nodes_list = load_maze()
    if save_var.get() == 1:
        HelperFile.save_canvas(root, canvas, file_path + ".png")
        solve_maze_text = PathFinder.solve_A_star(root, canvas, nodes_list, folder[1], float(pause_entry.get()),
                                                  draw_nodes_var.get(), draw_text_var.get(), movie_var.get())
        HelperFile.save_canvas(root, canvas, file_path + "_solved.png")
    else:
        solve_maze_text = PathFinder.solve_A_star(root, canvas, nodes_list, folder[1], float(pause_entry.get()),
                                                  draw_nodes_var.get(), draw_text_var.get(), create_frames=0)

    done_label.config(text=gen_text + save_text + load_text + "\n" + solve_maze_text, justify="left")
    save_box.deselect()
    print(HelperFile.convert_seq_to_mov()) if movie_var.get() == 1 else print()


root = Tk()
root.title("Maze Generator")
root.state("zoomed")
# root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

width = 1600
height = 1024
cell_size = 64
border = 4

width_button = 16
height_button = 3

rows = int(height / cell_size)
cols = int(width / cell_size)
grid = [Cell()]
cells_visited = []
cells_blocked = []

cell_current = Cell()
cell_next = Cell()
stack = []

gen_text = ""
save_text = ""
load_text = ""
solve_maze_text = ""

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

canvas = Canvas(root, width=width + border, height=height + border, bg="#cccccc")
canvas.grid(row=0, column=0, rowspan=rows, columnspan=cols)

done_label = Label(root, text="")
width_label = Entry(root)
height_label = Entry(root)
cell_size_label = Entry(root)
done_label.grid(row=0, column=cols + 1, columnspan=4, sticky="w")
width_label.grid(row=1, column=cols + 3, columnspan=2)
height_label.grid(row=2, column=cols + 3, columnspan=2)
cell_size_label.grid(row=3, column=cols + 3, columnspan=2)
width_label.insert(0, "max 1600")
height_label.insert(0, "max 1024")
cell_size_label.insert(0, "min 16")
width_text = Label(root, text="Width Maze")
height_text = Label(root, text="Height Maze")
cell_size_text = Label(root, text="Cell Size Maze")
width_text.grid(row=1, column=cols + 1, columnspan=1, sticky="w")
height_text.grid(row=2, column=cols + 1, columnspan=1, sticky="w")
cell_size_text.grid(row=3, column=cols + 1, columnspan=1, sticky="w")

resize_maze_button = Button(root, text="Resize Maze", command=resize_maze)
resize_maze_button.config(width=int(width_button), height=int(height_button))
resize_maze_button.grid(row=4, column=cols + 1, columnspan=2)

generate_button = Button(root, text="Generate New Maze", command=generate_maze)
generate_button.config(width=int(width_button), height=int(height_button))
generate_button.grid(row=4, column=cols + 3, columnspan=2)

file_name_label = Entry(root)
file_name_label.grid(row=5, column=cols + 3, columnspan=2)
file_name_label.insert(0, str(datetime.datetime.now().strftime("%Y-%m-%d_%H;%M")))
file_name_text = Label(root, text="Filename")
file_name_text.grid(row=5, column=cols + 1, sticky="w", columnspan=1)

load_maze_button = Button(root, text="Load Maze", command=load_maze)
load_maze_button.config(width=int(width_button), height=int(height_button))
load_maze_button.grid(row=6, column=cols + 1, columnspan=2)

save_button = Button(root, text="Save Maze", command=save_to_csv)
save_button.config(width=int(width_button), height=int(height_button))
save_button.grid(row=6, column=cols + 3, columnspan=2)

pause_label = Label(root, text="Pause")
pause_entry = Entry(root)
pause_entry.insert(0, "0")
pause_label.grid(row=7, column=cols + 1, sticky="w")
pause_entry.grid(row=7, column=cols + 3, sticky="e")

save_var = IntVar()
movie_var = IntVar()
draw_nodes_var = IntVar()
draw_text_var = IntVar()
save_box = Checkbutton(root, text='Save Maze', variable=save_var, onvalue=1, offvalue=0)
movie_box = Checkbutton(root, text='Create Movie', variable=movie_var, onvalue=1, offvalue=0)
draw_nodes_box = Checkbutton(root, text='Draw Nodes', variable=draw_nodes_var, onvalue=1, offvalue=0)
draw_text_box = Checkbutton(root, text='Draw Text', variable=draw_text_var, onvalue=1, offvalue=0)

save_box.grid(row=8, column=cols + 1, columnspan=2, sticky="w")
movie_box.grid(row=8, column=cols + 3, columnspan=2, sticky="w")
draw_nodes_box.grid(row=9, column=cols + 1, columnspan=2, sticky="w")
draw_text_box.grid(row=9, column=cols + 3, columnspan=2, sticky="w")

solve_maze_button = Button(root, text="Solve Maze", command=solve_maze)
solve_maze_button.config(width=int(width_button), height=int(height_button))
solve_maze_button.grid(row=10, column=cols + 1, columnspan=2)

exit_button = Button(root, text="Exit", command=close_window)
exit_button.config(width=int(width_button), height=int(height_button))
exit_button.grid(row=10, column=cols + 3, columnspan=2)

root.mainloop()
