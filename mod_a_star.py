import os
import math
import json
import copy 
import argparse
import numpy as np

# IO Utils
def read_input(input_path):
    with open(input_path, 'r') as f:
        data = json.load(f)
    return data["grid"], data["src_coor"], data["dest_coor"]

def write_output(output_dir, path_exists, path_length, path_coor):
    with open(os.path.join(output_dir, "mod_a_star.json"), 'w') as f:
        json.dump({
            "path_exists": path_exists,
            "path_length": path_length,
            "path_coor": path_coor
        }, f)

# Routing Utils
def is_equal(src_pt, dest_pt):
    return src_pt[0] == dest_pt[0] and \
        src_pt[1] == dest_pt[1] and \
        src_pt[2] == dest_pt[2] 

def get_cell_val(grid, pt):
    return grid[pt[0]][pt[1]][pt[2]]

def get_surroundings(src_pt, is_via, height, width):
    surround_pts = []
    if (src_pt[1]-1 >= 0):
        surround_pts.append([src_pt[0],src_pt[1]-1,src_pt[2]])
    if (src_pt[1]+1 < height):
        surround_pts.append([src_pt[0],src_pt[1]+1,src_pt[2]])
    if (src_pt[2]-1 >= 0):
        surround_pts.append([src_pt[0],src_pt[1],src_pt[2]-1])
    if (src_pt[2]+1 < width):
        surround_pts.append([src_pt[0],src_pt[1],src_pt[2]+1])
    if is_via:
        surround_pts.append([abs(src_pt[0]-1),src_pt[1],src_pt[2]])
    return surround_pts

def calc_euclid_dist(src_pt, dest_pt):
    return math.sqrt((src_pt[0]-dest_pt[0])**2 + \
                    (src_pt[1]-dest_pt[1])**2 + \
                    (src_pt[2]-dest_pt[2])**2)

# Routing
def solve_routing(grid, src_coor, dest_coor):
    print("Starting single layer routing ...")
    # output initialization
    src_points = [src_coor]
    path_exists = []
    path_length = []
    path_coor = []

    # loop over all destinations
    for dest_pt in dest_coor:
        print("Routing new destination")
        temp_src_points = copy.deepcopy(src_points)
        path_found = False

        # loop for destination or complete blockage
        while(True):
            path_cells = [] # cells along path from source to destination
            # find closest source cell
            if (len(temp_src_points) == 0):
                break
            src_cell = temp_src_points[0]
            src_dist = float("inf")
            for src_pt in temp_src_points:
                if calc_euclid_dist(src_pt, dest_pt) < src_dist:
                    src_cell = src_pt
                    src_dist = calc_euclid_dist(src_pt, dest_pt)
            path_cells.append(src_cell)
            temp_src_points.remove(src_cell)

            # loop for destination hit
            path_surround = dict() # all surroundings of current path
            while(True):
                # break of destination hit
                if is_equal(src_cell, dest_pt):
                    path_found = True
                    break
                # check is cell is already visited
                if tuple(src_cell) not in path_surround.keys():
                    is_via = (get_cell_val(grid, src_cell) == 2)
                    surround_pts = get_surroundings(src_cell, is_via, len(grid[0]), len(grid[0][0]))
                    path_surround[tuple(src_cell)] = surround_pts
                # loop to get closest surrounding to destination
                if (len(path_surround[tuple(src_cell)]) == 0):
                    del path_surround[tuple(src_cell)]
                    path_cells.remove(src_cell)
                    src_cell = path_cells[-1]
                temp_src_cell = path_surround[tuple(src_cell)][0]
                src_dist = float("inf")
                for src_pt in path_surround[tuple(src_cell)]:
                    if calc_euclid_dist(src_pt, dest_pt) < src_dist and \
                        get_cell_val(grid, src_pt) != 1 and \
                        tuple(src_pt) not in path_surround.keys():
                        temp_src_cell = src_pt
                        src_dist = calc_euclid_dist(src_pt, dest_pt)
                if src_dist != float("inf"):
                    path_cells.append(temp_src_cell)
                    path_surround[tuple(src_cell)].remove(temp_src_cell)
                    src_cell = temp_src_cell
                else:
                    del path_surround[tuple(src_cell)]
                    path_cells.remove(src_cell)
                    if (len(path_cells) == 0):
                        break
                    else:
                        src_cell = path_cells[-1]

            # check if a path is found
            if path_found:
                # append path cells to output
                path_exists.append(True)
                path_length.append(len(path_cells))
                path_coor.append(path_cells)
                # add current path to source points
                src_points.extend(path_cells)
                break
        
        # check if path isn't found
        if path_found:
            path_exists.append(False)
            path_length.append(0)
            path_coor.append([])

    return path_exists, path_length, path_coor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--in_path', help='path to input json', default='inputs/test1.json')
    parser.add_argument('--out_dir', help='path to output json', default='outputs/')
    
    args = parser.parse_args()

    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    grid, src_coor, dest_coor = read_input(args.in_path)

    if len(grid) == 1 or len(grid) == 2:
        path_exists, path_length, path_coor = solve_routing(grid, src_coor, dest_coor)
    else:
        print("Invalid depth!")

    write_output(args.out_dir, path_exists, path_length, path_coor)