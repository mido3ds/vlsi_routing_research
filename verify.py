#!/bin/env python3
'''
Verify if given output solves given input case. Makes sure that:
0. All points are valid in range.
1. Lenghtes are non-negative.
2. Lengthes match len(path_coor)
3. The final point in each path is one of the terminals in dest_coor or a point in other path that leads to it.
4. The first point in each path is src_coor or a point in other path that leads to it.
5. No path goes over an obstacle.
6. Number of elements "path_exists", "path_length" and "path_coor" must be equal to len(dest_coor)

Requirements:
    - python3 3.8.2
    - python3-pip 20.0.2

Example: python verify.py inputs/test1.json outputs/mikami_tabuchi/test1.json
'''
import argparse
import json
import random
import sys
from argparse import RawTextHelpFormatter

# colors
RESET = '\033[00m'
RED = '\033[31m'
GREEN = '\033[32m'
Yellow = '\u001b[33m'


def ok(msg): return print(GREEN + 'ok:' + RESET, msg)


def warn(msg): return print(Yellow + 'warn:' + RESET, msg)


def get_dimensions(grid) -> (int, int, int):
    # d, h, w
    return len(grid), len(grid[0]), len(grid[0][0])


def check_sizes(dest_coor, path_exists, path_length, path_coor):
    assert len(dest_coor) == len(path_exists) == len(path_length) == len(path_coor), \
        'Number of elements "path_exists", "path_length" and "path_coor" must be equal to len(dest_coor)'
    ok('arrays sizes')


def check_valid_ranges(d, h, w, path_coor):
    for coor in path_coor:
        for point in coor:
            assert point[0] < d and point[1] >= 0, f'point({point}) out of range in d({d})'
            assert point[1] < h and point[1] >= 0, f'point({point}) out of range in h({h})'
            assert point[2] < w and point[1] >= 0, f'point({point}) out of range in w({w})'
    ok('all points are valid in ranges')


def check_lengthes(path_length, path_coor):
    fail = False
    for i, l in enumerate(path_length):
        assert l >= 0, 'lengthes must be positive'
        if not len(path_coor[i]) == l:
            warn(f'length({i})={l} != len(path_coor[{i}])={len(path_coor[i])}')
            fail = True

    if not fail:
        ok('all path_length are positive and match the length of path_coor')
    else:
        ok('all path_length are positive')


def exists_in_non_i(i: int, x: object, ys: [[object]]) -> bool:
    for i2, y in enumerate(ys):
        if x in y and i != i2:
            return True
    return False


def check_start_terminals(src_coor, path_coor):
    fail = False
    for i, path in enumerate(path_coor):
        if len(path) != 0:
            if not path[0] == src_coor:
                warn(f'path_coor[{i}] first point={path[0]}'
                     f' is not src_coor={src_coor}')

                assert exists_in_non_i(i, path[0], path_coor),\
                    f'path_coor[{i}] first point={path[0]}'\
                    f' doest have any connection to src_coor={src_coor}'

                fail = True

    if not fail:
        ok('all path_coor start with src_coor')
    else:
        ok('all path_coor at least start with a point that connects to src_coor')


def check_end_terminals(dest_coor, path_coor):
    fail = False
    examined_coords = []
    for i, path in enumerate(path_coor):
        if len(path) != 0:
            if not path[-1] in dest_coor:
                warn(f'path_coor[{i}] leads to a point that doesnt belong '
                     f'to the final terminals, point={path[-1]}, final terminals={dest_coor}')
                assert exists_in_non_i(i, path[-1], path_coor),\
                    f'path_coor[{i}] doesnt lead to a point that belong '\
                    f'to the final terminals, point={path[-1]}, final terminals={dest_coor}'
                fail = True

            assert path[-1] not in examined_coords,\
                f'path_length[{i}] leads to a duplicate end point={path[-1]}'
            examined_coords.append(path[-1])

    if not fail:
        ok('all path_coor end with one dest_coor, no duplication')
    else:
        ok('all path_coor have some connection to one dest_coor, no duplication')


def is_adjacent(a: [int], b: [int]) -> bool:
    return abs(sum([a[i] - b[i] for i in range(3)])) == 1


def on_obstacle(a: [int], grid) -> bool:
    return grid[a[0]][a[1]][a[2]] == 1


def check_adjacent(path_coor):
    for i, path in enumerate(path_coor):
        for j in range(len(path)-1):
            assert is_adjacent(path[j], path[j+1]),\
                f'path_coor[{i}][{j}]={path[j]} and path_coor[{i}][{j+1}]={path[j+1]} are not adjacent'
    ok('all points in all path_coor are adjacent')


def check_obstacles(grid, path_coor):
    for i, path in enumerate(path_coor):
        for j, point in enumerate(path):
            assert not on_obstacle(point, grid), \
                f'path_coor[{i}][{j}]={point} is on an obstacle'
    ok('all points in all path_coor are not on an obstacle')


# args
parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=RawTextHelpFormatter
)
parser.add_argument('input', help='path to input json')
parser.add_argument('output', help='path to output json')

args = parser.parse_args()

# files
with open(args.input, 'r') as f:
    inp = json.load(f)
    dest_coor = inp['dest_coor']
    src_coor = inp['src_coor']
    grid = inp['grid']
    d, h, w = get_dimensions(grid)

with open(args.output, 'r') as f:
    out = json.load(f)
    path_length = out['path_length']
    path_exists = out['path_exists']
    path_coor = out['path_coor']

# verification
try:
    check_sizes(dest_coor, path_exists,
                path_length, path_coor)
    check_valid_ranges(d, h, w, path_coor)
    check_lengthes(path_length, path_coor)
    check_start_terminals(src_coor, path_coor)
    check_end_terminals(dest_coor, path_coor)
    check_adjacent(path_coor)
    check_obstacles(grid, path_coor)
except AssertionError as e:
    print(RED, 'fail: ', RESET, e, sep='')
    exit(1)

print('verified all')
