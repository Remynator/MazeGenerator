from PIL import ImageGrab
import os
import subprocess
import math


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


def distance(node_a, node_b):
    return math.sqrt((node_a.i - node_b.i) ** 2 + (node_a.j - node_b.j) ** 2) * 10


def heuristic(node_a, node_b):
    h = (abs(node_a.i - node_b.i) + abs(node_a.j - node_b.j)) * 10
    # h = int(math.sqrt((node_a.i - node_b.i) ** 2 + (node_a.j - node_b.j) ** 2) * 10)
    return h


def create_new_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except OSError:
        print('Error: Creating directory. ' + folder_path)


def save_canvas(root, widget, filename):
    x = root.winfo_rootx() + widget.winfo_x()
    y = root.winfo_rooty() + widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)


def convert_seq_to_mov():
    input_path = os.path.join("frames", "frame%04d.png")
    output_path = os.path.join("video.mp4")
    frame_rate = 6
    cmd = f'ffmpeg -framerate {frame_rate} -i "{input_path}" "{output_path}"'
    t = False
    if t:
        subprocess.check_output(cmd, shell=True)
    return cmd
