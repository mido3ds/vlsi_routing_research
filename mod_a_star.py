import os
import math
import json
import argparse
import numpy as np

# IO Utils
def read_input(input_path):
    with open(input_path, 'r') as f:
        data = json.load(f)
    return np.array(data["grid"]), np.array(data["src_coor"]), np.array(data["dest_coor"])

def write_output(output_dir, path_exists, path_length, path_coor):
    with open(os.path.join(output_dir, "mod_a_star.json"), 'w') as f:
        json.dump({
            "path_exists": path_exists,
            "path_length": path_length,
            "path_coor": path_coor
        }, f)

# Routing Utils
def is_equal(src_pt, dest_pt):
    return src_pt[0] == dest_pt[0] and src_pt[1] == dest_pt[1] and src_pt[2] == dest_pt[2] 

def get_cell_val(grid, pt):
    return grid[pt[0],pt[1],pt[2]]

def get_surroundings(src_pt, is_via):
    surround_pts = [np.array([src_pt[0],src_pt[1]-1,src_pt[2]]),
                    np.array([src_pt[0],src_pt[1]+1,src_pt[2]]),
                    np.array([src_pt[0],src_pt[1],src_pt[2]-1]),
                    np.array([src_pt[0],src_pt[1],src_pt[2]+1])]
    if is_via:
        surround_pts.append(np.array([abs(src_pt[0]-1),src_pt[1],src_pt[2]]))
    return surround_pts

def calc_euclid_dist(src_pt, dest_pt):
    pt_diff = src_pt - dest_pt
    return math.sqrt(pt_diff[0]**2 + pt_diff[1]**2 + pt_diff[2]**2)

# Routing
def solve_routing(grid, src_coor, dest_coor):
    print("Starting single layer routing ...")
    # output initialization
    src_points = [src_coor]
    path_exists = []
    path_length = []
    path_coor = []
    # loop over all destinations
    for dest_pt in list(dest_coor):
        print("Routing new destination")
        # find closest source cell
        path_cells = []
        src_cell = src_points[0]
        src_dist = float("inf")
        for src_pt in src_points:
            if calc_euclid_dist(src_pt, dest_pt) < src_dist:
                src_cell = src_pt
                src_dist = calc_euclid_dist(src_pt, dest_pt)
        path_cells.append(src_cell.tolist())
        # loop till destination hit
        while(True):
            if is_equal(src_cell, dest_pt):
                break
            is_via = (get_cell_val(grid, src_cell) == 2)
            surround_pts = get_surroundings(src_cell, is_via)
            src_cell = surround_pts[0]
            src_dist = float("inf")
            for src_pt in surround_pts:
                if calc_euclid_dist(src_pt, dest_pt) < src_dist:
                    src_cell = src_pt
                    src_dist = calc_euclid_dist(src_pt, dest_pt)
            path_cells.append(src_cell.tolist())
        # append path cells to output
        path_exists.append(True)
        path_length.append(len(path_cells))
        path_coor.append(path_cells)

    return path_exists, path_length, path_coor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--in_path', help='path to input json', default='inputs/test1.json')
    parser.add_argument('--out_dir', help='path to output json', default='outputs/')
    
    args = parser.parse_args()

    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    grid, src_coor, dest_coor = read_input(args.in_path)

    if grid.shape[0] == 1 or grid.shape[0] == 2:
        path_exists, path_length, path_coor = solve_routing(grid, src_coor, dest_coor)
    else:
        print("Invalid depth!")

    write_output(args.out_dir, path_exists, path_length, path_coor)