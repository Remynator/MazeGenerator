import os
import time
import ConfigFiles.Config as cfg


def find_nodes():
    for i in range(len(cfg.grid)):
        cell = cfg.grid[i]

        if not cell.walls[0] == cell.walls[2] or not cell.walls[1] == cell.walls[3] or cell.start or cell.end or (
                cell.walls[0] == cell.walls[1] and cell.walls[0] == cell.walls[2] and cell.walls[0] == cell.walls[3]):
            cell.is_node = True
            cell.index_node = len(cfg.node_list)

            node = cfg.Node(cell.i, cell.j, cell.w)
            node.start = cell.start
            node.end = cell.end
            node.index = len(cfg.node_list)
            node.canvas = [None, None, None, None, None, None, None, None]
            cfg.node_list.append(node)

            # node.draw_node(draw_nodes_var.get(), draw_text_var.get())
        else:
            cell.is_node = False
            cell.index_node = None


def connect_nodes():
    for i in range(len(cfg.node_list)):
        start_node = cfg.node_list[i]
        start_cell = cfg.grid[cfg.index(start_node.j, start_node.i)]

        if not start_cell.walls[1]:
            for j in range(start_cell.i + 1, cfg.cols):
                check_cell = cfg.grid[cfg.index(start_cell.j, j)]

                if check_cell.is_node:
                    check_node = cfg.node_list[check_cell.index_node]
                    start_node.connect[1] = check_node
                    check_node.connect[3] = start_node
                    break

        if not start_cell.walls[2]:
            for j in range(start_cell.j + 1, cfg.rows):
                check_cell = cfg.grid[cfg.index(j, start_cell.i)]

                if check_cell.is_node:
                    check_node = cfg.node_list[check_cell.index_node]
                    start_node.connect[2] = check_node
                    check_node.connect[0] = start_node
                    break


def solve_A_star(pause_solver, draw_node, draw_text, create_frames):
    from Menu.FileMenu import create_new_folder

    frame_path = os.path.join(os.path.dirname(cfg.maze_path), "Frames")
    frame_nr = -1

    open_set = []
    closed_set = []

    index_start = 0
    node_start = cfg.node_list[0]
    node_end = cfg.node_list[len(cfg.node_list) - 1]

    for i in range(len(cfg.node_list)):
        if cfg.node_list[i].start:
            index_start = i
            node_start = cfg.node_list[i]

        if cfg.node_list[i].end:
            node_end = cfg.node_list[i]

    node_start.g = int(0)
    node_start.heuristic(node_end)
    node_start.f = int(node_start.g + node_start.h)

    node_current = node_start
    open_set.append(node_current)
    node_current.in_open = True

    while len(open_set) > 0 and not node_current.end:
        time.sleep(pause_solver)
        if create_frames == 1:
            create_new_folder(frame_path)
            frame_nr += 1
            cfg.save_canvas(cfg.canvas, os.path.join(frame_path, "frame" + str(frame_nr).zfill(4) + ".png"))

        open_set = sorted(open_set, key=lambda x: (x.f, x.h))

        node_current = open_set[0]
        open_set.pop(0)
        node_current.in_open = False
        closed_set.append(node_current)
        node_current.in_closed = True
        node_current.draw_node(draw_node, draw_text)

        for i in range(len(node_current.connect)):
            neighbor = node_current.connect[i]

            if neighbor is not None and neighbor not in closed_set:
                temp_g = node_current.g + node_current.distance(neighbor)

                if neighbor in open_set:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                        neighbor.parent = node_current
                    neighbor.heuristic(node_end)
                    neighbor.f = int(neighbor.g + neighbor.h)
                else:
                    neighbor.g = int(temp_g)
                    neighbor.heuristic(node_end)
                    neighbor.f = int(neighbor.g + neighbor.h)
                    open_set.append(neighbor)
                    neighbor.in_open = True
                    neighbor.parent = node_current

                neighbor.draw_node(draw_node, draw_text)

        if node_current.end:
            path = []
            temp_node = node_current
            path.append(temp_node)
            temp_node.is_path = True
            cfg.node_list[index_start].is_path = True

            while temp_node.parent is not None:
                time.sleep(pause_solver)
                path.append(temp_node.parent)
                temp_node.is_path = True
                temp_node.connect_nodes(temp_node.parent)
                temp_node.draw_node(draw_node, draw_text)
                temp_node = temp_node.parent
                if create_frames == 1:
                    frame_nr += 1
                    cfg.save_canvas(cfg.canvas, os.path.join(frame_path, "frame" + str(frame_nr).zfill(4) + ".png"))

            for k in range(12):
                frame_nr += 1
                cfg.save_canvas(cfg.canvas, os.path.join(frame_path, "frame" + str(frame_nr).zfill(4) + ".png"))

            return "Maze Solved Shortest Path: " + str(int(node_current.f))

        if len(open_set) == 0 and not node_current.end:
            return "No Solution"


def solve_maze():
    from Menu.FileMenu import file_menu_save
    cfg.canvas.delete("all")
    cfg.draw_all_cells(cfg.grid)

    find_nodes()
    connect_nodes()

    cfg.gen_text = "Maze Generated: " + str(cfg.rows) + " R by " + str(cfg.cols) + " C, Cell size: " + str(
        cfg.cell_size)
    cfg.load_text = "\nMaze Loaded: " + str(len(cfg.node_list)) + "/" + str(cfg.rows * cfg.cols) + " Nodes"
    cfg.info_label.config(text=cfg.gen_text + cfg.save_text + cfg.load_text, justify="left")
    cfg.root.update()

    pause_val = float(cfg.pause_entry.get())
    is_draw_nodes = cfg.draw_nodes_var.get()
    is_draw_text = cfg.draw_text_var.get()
    is_movie = cfg.movie_var.get()

    file_menu_save()
    file_path, file_extension = os.path.splitext(cfg.maze_path)
    cfg.save_canvas(cfg.canvas, file_path + ".png")

    solve_maze_text = solve_A_star(pause_val, is_draw_nodes, is_draw_text, is_movie)

    cfg.save_canvas(cfg.canvas, file_path + "_solved.png")

    cfg.info_label.config(text=cfg.gen_text + cfg.save_text + cfg.load_text + "\n" + solve_maze_text, justify="left")
    cfg.save_box.deselect()
    print(cfg.convert_seq_to_mov()) if cfg.movie_var.get() == 1 else print()
