import os
import json
import argparse
import numpy as np

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

def solve_one_layer(grid, src_coor, dest_coor):
    return 1, 2, 3

def solve_two_layer(grid, src_coor, dest_coor):
    return 1, 2, 3


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--in_path', help='path to input json', default='inputs/test1.json')
    parser.add_argument('--out_dir', help='path to output json', default='outputs/')
    
    args = parser.parse_args()

    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    grid, src_coor, dest_coor = read_input(args.in_path)

    if grid.shape[0] == 1:
        path_exists, path_length, path_coor = solve_one_layer(grid, src_coor, dest_coor)
    elif grid.shape[0] == 2:
        path_exists, path_length, path_coor = solve_two_layer(grid, src_coor, dest_coor)
    else:
        print("Invalid depth!")

    write_output(args.out_dir, path_exists, path_length, path_coor)