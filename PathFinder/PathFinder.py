import PathFinder.HelperFile as hf
import os
import time


def solve_A_star(root, canvas, nodes_list, folder, pause_solver, draw_node, draw_text, create_frames):
    frame_nr = -1
    frame_path = os.path.join(folder, "frames")

    open_set = []
    closed_set = []

    index_start = 0
    node_start = nodes_list[0]
    node_end = nodes_list[len(nodes_list) - 1]

    for i in range(len(nodes_list)):
        if nodes_list[i].start:
            index_start = i
            node_start = nodes_list[i]

        if nodes_list[i].end:
            node_end = nodes_list[i]

    node_start.g = int(0)
    node_start.h = hf.heuristic(node_start, node_end)
    node_start.f = int(node_start.g + node_start.h)

    node_current = node_start
    open_set.append(node_current)
    node_current.in_open = True

    while len(open_set) > 0 and not node_current.end:
        time.sleep(pause_solver)
        if create_frames == 1:
            hf.create_new_folder(frame_path)
            frame_nr += 1
            hf.save_canvas(root, canvas, os.path.join(frame_path, "frame" + str(frame_nr).zfill(4) + ".png"))

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
                temp_g = node_current.g + hf.distance(node_current, neighbor)

                if neighbor in open_set:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                        neighbor.parent = node_current
                    neighbor.h = hf.heuristic(neighbor, node_end)
                    neighbor.f = int(neighbor.g + neighbor.h)
                else:
                    neighbor.g = int(temp_g)
                    neighbor.h = hf.heuristic(neighbor, node_end)
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
            nodes_list[index_start].is_path = True

            while temp_node.parent is not None:
                time.sleep(pause_solver)
                path.append(temp_node.parent)
                temp_node.is_path = True
                temp_node.connect_nodes()
                temp_node.draw_node(draw_node, draw_text)
                temp_node = temp_node.parent
                if create_frames == 1:
                    frame_nr += 1
                    hf.save_canvas(root, canvas, os.path.join(frame_path, "frame" + str(frame_nr).zfill(4) + ".png"))

            return "Maze Solved Shortest Path: " + str(int(node_current.f))

        if len(open_set) == 0 and not node_current.end:
            return "No Solution"
