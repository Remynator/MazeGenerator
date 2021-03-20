import os
import pandas as pd
from tkinter import *
from tkinter import filedialog
from ConfigFiles import Config as cfg


def create_new_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except OSError:
        print('Error: Creating directory. ' + folder_path)


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


def file_menu_open():
    file_menu_close()

    initial_dir = os.path.join(cfg.root_dir, "Mazes")
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Open File", filetypes=(
        ("csv File", "*.csv"), ("All Files", "*.*")))

    if file_path:
        cfg.maze_path = file_path
        file_path = file_path.replace("/", "\\")
        file_name = file_path.replace(os.path.dirname(file_path) + "\\", "")
        cfg.maze_name = file_name

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
        cfg.draw_all_cells(cfg.grid)

        last_cell = cfg.grid[len(cfg.grid) - 1]
        cfg.rows = last_cell.j + 1
        cfg.cols = last_cell.i + 1
        cfg.cell_size = last_cell.w
        cfg.width = cfg.cols * cfg.cell_size
        cfg.height = cfg.rows * cfg.cell_size

        cfg.canvas.config(width=cfg.width + cfg.border, height=cfg.height + cfg.border, bg="#cccccc")

        cfg.gen_text = "Maze Generated: " + str(cfg.rows) + " R by " + str(cfg.cols) + " C, Cell size: " + str(
            cfg.cell_size)
        cfg.save_text = "\nMaze Opened: " + cfg.maze_name
        cfg.info_label.config(text=cfg.gen_text + cfg.save_text, justify="left")


def file_menu_save():
    if cfg.maze_path:
        if cfg.maze_path.lower().endswith('.csv'):
            write_csv_file(cfg.maze_path)

        cfg.save_text = "\nMaze Saved: " + cfg.maze_name
        cfg.info_label.config(text=cfg.gen_text + cfg.save_text, justify="left")
    else:
        file_menu_save_as()


def file_menu_save_as():
    initial_dir = os.path.join(cfg.root_dir, "Mazes")
    file_path = filedialog.asksaveasfilename(defaultextension=".*", initialdir=initial_dir, title="Save as File",
                                             filetypes=(("csv File", "*.csv"), ("All Files", "*.*")))

    if file_path:
        file_path = file_path.replace("/", "\\")
        file_name = file_path.replace(os.path.dirname(file_path) + "\\", "")

        cfg.maze_path = file_path
        cfg.maze_name = file_name
        folder_path, file_extension = os.path.splitext(file_path)
        file_path = os.path.join(folder_path, file_name)

        if file_name.lower().endswith('.csv'):

            try:
                pd.read_csv(file_path)
            except FileNotFoundError:
                create_new_folder(folder_path)

            write_csv_file(file_path)

            cfg.save_text = "\nMaze Saved as: " + cfg.maze_name
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


def file_menu_close():
    cfg.canvas.delete("all")
    cfg.grid.clear()
    cfg.node_list.clear()
    cfg.maze_path = False
    cfg.status_bar.config(text=f'Closed: {cfg.maze_name}      ')

