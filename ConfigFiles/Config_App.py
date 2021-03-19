import datetime
from tkinter import *
from ConfigFiles import Config as cfg


def setup_canvas():
    from MazeGenerator import resize_maze, generate_maze, load_maze, save_to_csv, solve_maze

    cfg.root.title("Maze Generator")
    # cfg.root.state("zoomed")
    # root.attributes("-fullscreen", True)
    cfg.root.bind("<F11>", lambda event: cfg.root.attributes("-fullscreen", not cfg.root.attributes("-fullscreen")))
    cfg.root.bind("<Escape>", lambda event: cfg.root.attributes("-fullscreen", False))

    width_button = 16
    height_button = 3

    cfg.canvas = Canvas(cfg.root, width=cfg.width + cfg.border, height=cfg.height + cfg.border, bg="#cccccc")
    cfg.canvas.grid(row=0, column=0, rowspan=cfg.rows * 2, columnspan=cfg.cols)

    cfg.info_label = Label(cfg.root, text="")
    cfg.width_label = Entry(cfg.root)
    cfg.height_label = Entry(cfg.root)
    cfg.cell_size_label = Entry(cfg.root)
    cfg.info_label.grid(row=0, column=cfg.cols + 1, columnspan=4, sticky="w")
    cfg.width_label.grid(row=1, column=cfg.cols + 3, columnspan=2)
    cfg.height_label.grid(row=2, column=cfg.cols + 3, columnspan=2)
    cfg.cell_size_label.grid(row=3, column=cfg.cols + 3, columnspan=2)
    cfg.width_label.insert(0, "max 1600")
    cfg.height_label.insert(0, "max 1024")
    cfg.cell_size_label.insert(0, "min 16")
    width_text = Label(cfg.root, text="Width Maze")
    height_text = Label(cfg.root, text="Height Maze")
    cell_size_text = Label(cfg.root, text="Cell Size Maze")
    width_text.grid(row=1, column=cfg.cols + 1, columnspan=1, sticky="w")
    height_text.grid(row=2, column=cfg.cols + 1, columnspan=1, sticky="w")
    cell_size_text.grid(row=3, column=cfg.cols + 1, columnspan=1, sticky="w")

    # TODO convert buttons to menu

    resize_maze_button = Button(cfg.root, text="Resize Maze", command=resize_maze)
    resize_maze_button.config(width=int(width_button), height=int(height_button))
    resize_maze_button.grid(row=4, column=cfg.cols + 1, columnspan=2)

    generate_button = Button(cfg.root, text="Generate New Maze", command=generate_maze)
    generate_button.config(width=int(width_button), height=int(height_button))
    generate_button.grid(row=4, column=cfg.cols + 3, columnspan=2)

    load_maze_button = Button(cfg.root, text="Load Maze", command=load_maze)
    load_maze_button.config(width=int(width_button), height=int(height_button))
    load_maze_button.grid(row=6, column=cfg.cols + 1, columnspan=2)

    save_button = Button(cfg.root, text="Save Maze", command=save_to_csv)
    save_button.config(width=int(width_button), height=int(height_button))
    save_button.grid(row=6, column=cfg.cols + 3, columnspan=2)

    pause_label = Label(cfg.root, text="Pause")
    pause_label.grid(row=7, column=cfg.cols + 1, sticky="w")
    cfg.pause_entry = Entry(cfg.root)
    cfg.pause_entry.insert(0, "0")
    cfg.pause_entry.grid(row=7, column=cfg.cols + 3, sticky="e")

    cfg.save_var = IntVar()
    cfg.movie_var = IntVar()
    cfg.draw_nodes_var = IntVar()
    cfg.draw_text_var = IntVar()
    save_box = Checkbutton(cfg.root, text='Save Maze', variable=cfg.save_var, onvalue=1, offvalue=0)
    movie_box = Checkbutton(cfg.root, text='Create Movie', variable=cfg.movie_var, onvalue=1, offvalue=0)
    draw_nodes_box = Checkbutton(cfg.root, text='Draw Nodes', variable=cfg.draw_nodes_var, onvalue=1, offvalue=0)
    draw_text_box = Checkbutton(cfg.root, text='Draw Text', variable=cfg.draw_text_var, onvalue=1, offvalue=0)

    save_box.grid(row=8, column=cfg.cols + 1, columnspan=2, sticky="w")
    movie_box.grid(row=8, column=cfg.cols + 3, columnspan=2, sticky="w")
    draw_nodes_box.grid(row=9, column=cfg.cols + 1, columnspan=2, sticky="w")
    draw_text_box.grid(row=9, column=cfg.cols + 3, columnspan=2, sticky="w")

    solve_maze_button = Button(cfg.root, text="Solve Maze", command=solve_maze)
    solve_maze_button.config(width=int(width_button), height=int(height_button))
    solve_maze_button.grid(row=10, column=cfg.cols + 1, columnspan=2)

    exit_button = Button(cfg.root, text="Exit", command=cfg.root.destroy)
    exit_button.config(width=int(width_button), height=int(height_button))
    exit_button.grid(row=10, column=cfg.cols + 3, columnspan=2)
