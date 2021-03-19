import os
import time
import pandas as pd
import random
from tkinter import *
from tkinter import filedialog
from ConfigFiles import Config as cfg
import PathFinder.PathFinder as PathFinder
import PathFinder.HelperFile as HelperFile


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


def generate_maze():
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
            HelperFile.remove_walls(cfg.cell_current, cell_next)

            # STEP 1.4
            cfg.cell_current.draw_cell()
            cfg.cell_current = cell_next
            cell_next.draw_cell()
        elif len(stack) > 0:
            # 2.1 # 2.2
            cfg.cell_current = stack.pop()

        time.sleep(0)

    cfg.gen_text = "Maze Generated: " + str(cfg.rows) + " R by " + str(cfg.cols) + " C, Cell size: " + str(cfg.cell_size)
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


def write_csv_file(file_path):

    f = open(file_path, "w+")
    # create header
    f.write("col_nr,row_nr,cell_size,visited,blocked,start,end,wall_top,wall_right,wall_bottom,wall_left\n")

    # loop though all cells

    for i in range(len(cfg.grid)):
        write_cell = cfg.grid[i]
        f.write(str(write_cell.i) + "," +
                str(write_cell.j) + "," +
                str(write_cell.w) + "," +
                str(write_cell.visited) + "," +
                str(write_cell.blocked) + "," +
                str(write_cell.start) + "," +
                str(write_cell.end) + "," +
                str(write_cell.walls[0]) + "," +
                str(write_cell.walls[1]) + "," +
                str(write_cell.walls[2]) + "," +
                str(write_cell.walls[3]) + "\n")

    f.close()


def read_csv_file(file_path):
    df = pd.read_csv(file_path)
    array = df.to_numpy()
    cell_list = []

    for i in range(len(array)):
        # col_nr, row_nr, visited, cell_size, blocked, start, end, wall_top, wall_right, wall_bottom, wall_left
        cell = cfg.Cell(array[i][0], array[i][1], array[i][2])
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

    return cell_list


def save_to_csv():
    initial_dir = os.path.join(cfg.root_dir, "Mazes")
    file_path = filedialog.asksaveasfilename(defaultextension=".*", initialdir=initial_dir, title="Save as File",
                                             filetypes=(("csv File", "*.csv"), ("All Files", "*.*")))
    file_path = file_path.replace("/", "\\")
    file_name = file_path.replace(os.path.dirname(file_path) + "\\", "")

    folder_path, file_extension = os.path.splitext(file_path)
    file_path = os.path.join(folder_path, file_name)

    if file_name.lower().endswith('.csv'):

        try:
            pd.read_csv(file_path)
        except FileNotFoundError:
            HelperFile.create_new_folder(folder_path)

            write_csv_file(file_path)

            cfg.save_text = "\nMaze Saved as: " + file_name
            cfg.info_label.config(text=cfg.gen_text + cfg.save_text, justify="left")
    else:
        extension_popup = Toplevel(cfg.root)
        extension_popup.title("Wrong extension")
        extension_popup.geometry("250x100")

        msg = "Please save as .csv file"

        extension_popup_label = Label(extension_popup, text=msg)
        extension_popup_label.pack(pady=10)

        extension_popup_ok = Button(extension_popup, text="Ok", padx=10, pady=5, command=extension_popup.destroy)
        extension_popup_ok.pack()

    return folder_path, folder_path


def load_maze():
    initial_dir = os.path.join(cfg.root_dir, "Mazes")
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Open File", filetypes=(
        ("csv File", "*.csv"), ("All Files", "*.*")))

    if file_path:
        file_path = file_path.replace("/", "\\")
        file_name = file_path.replace(os.path.dirname(file_path) + "\\", "")

        folder_path = os.path.dirname(file_path)
        # file_path = os.path.join(folder_path, file_name)

        if file_name.lower().endswith('.csv'):
            cfg.grid = read_csv_file(file_path)
        else:
            extension_popup = Toplevel(cfg.root)
            extension_popup.title("Wrong extension")
            extension_popup.geometry("250x100")

            msg = "Please selected a .csv file"

            extension_popup_label = Label(extension_popup, text=msg)
            extension_popup_label.pack(pady=10)

            extension_popup_ok = Button(extension_popup, text="Ok", padx=10, pady=5, command=extension_popup.destroy)
            extension_popup_ok.pack()

        cfg.canvas.delete("all")
        draw_all_cells(cfg.grid)

        last_cell = cfg.grid[len(cfg.grid) - 1]
        cfg.width = (last_cell.i + 1) * last_cell.w
        cfg.height = (last_cell.j + 1) * last_cell.w

        cfg.canvas.config(width=cfg.width + cfg.border, height=cfg.height + cfg.border, bg="#cccccc")

        cell_nodes = find_nodes(cfg.grid)
        node_list = connect_nodes(cell_nodes[0], cell_nodes[1])

        cfg.gen_text = "Maze Generated: " + str(cfg.rows) + " R by " + str(cfg.cols) + " C, Cell size: " + str(cfg.cell_size)
        cfg.load_text = "\nMaze Loaded: " + str(len(node_list)) + "/" + str(cfg.rows * cfg.cols) + " Nodes"
        cfg.info_label.config(text=cfg.gen_text + cfg.save_text + cfg.load_text, justify="left")
        cfg.root.update()

        return node_list


def draw_all_cells(cell_list):
    for i in range(len(cell_list)):
        cell = cell_list[i]
        cell.draw_cell()


def find_nodes(cell_list):
    nodes_list = []

    for i in range(len(cell_list)):
        cell = cell_list[i]

        if not cell.walls[0] == cell.walls[2] or not cell.walls[1] == cell.walls[3] or cell.start or cell.end or (
                cell.walls[0] == cell.walls[1] and cell.walls[0] == cell.walls[2] and cell.walls[0] == cell.walls[3]):
            cell.is_node = True
            cell.index_node = len(nodes_list)

            node = cfg.Node(cell.i, cell.j, cell.w)
            node.start = cell.start
            node.end = cell.end
            node.index = len(nodes_list)
            node.canvas = [None, None, None, None, None, None, None, None]
            nodes_list.append(node)

            # node.draw_node(draw_nodes_var.get(), draw_text_var.get())
        else:
            cell.is_node = False
            cell.index_node = None

    last_cell = cell_list[len(cell_list) - 1]
    cfg.rows = last_cell.j + 1
    cfg.cols = last_cell.i + 1

    return cell_list, nodes_list


def connect_nodes(cell_list, nodes_list):
    last_cell = cell_list[len(cell_list) - 1]
    cfg.rows = int(last_cell.j + 1)
    cfg.cols = int(last_cell.i + 1)

    for i in range(len(nodes_list)):
        start_node = nodes_list[i]
        start_cell = cell_list[cfg.index(start_node.j, start_node.i)]

        if not start_cell.walls[1]:
            for j in range(start_cell.i + 1, cfg.cols):
                check_cell = cell_list[cfg.index(start_cell.j, j)]

                if check_cell.is_node:
                    check_node = nodes_list[check_cell.index_node]
                    start_node.connect[1] = check_node
                    check_node.connect[3] = start_node
                    break

        if not start_cell.walls[2]:
            for j in range(start_cell.j + 1, cfg.rows):
                check_cell = cell_list[cfg.index(j, start_cell.i)]

                if check_cell.is_node:
                    check_node = nodes_list[check_cell.index_node]
                    start_node.connect[2] = check_node
                    check_node.connect[0] = start_node
                    break

        # start_node.connect_nodes()
        # start_node.draw_node(draw_nodes_var.get(), draw_text_var.get())

    return nodes_list


def solve_maze():
    folder = save_to_csv()
    file_path = os.path.join(folder[1], folder[0])

    nodes_list = load_maze()
    if cfg.save_var.get() == 1:
        HelperFile.save_canvas(cfg.root, cfg.canvas, file_path + ".png")
        solve_maze_text = PathFinder.solve_A_star(nodes_list, folder[1], float(cfg.pause_entry.get()),
                                                  cfg.draw_nodes_var.get(), cfg.draw_text_var.get(), cfg.movie_var.get())
        HelperFile.save_canvas(cfg.root, cfg.canvas, file_path + "_solved.png")
    else:
        solve_maze_text = PathFinder.solve_A_star(nodes_list, folder[1], float(cfg.pause_entry.get()),
                                                  cfg.draw_nodes_var.get(), cfg.draw_text_var.get(), create_frames=0)

    cfg.info_label.config(text=cfg.gen_text + cfg.save_text + cfg.load_text + "\n" + solve_maze_text, justify="left")
    cfg.save_box.deselect()
    print(HelperFile.convert_seq_to_mov()) if cfg.movie_var.get() == 1 else print()
