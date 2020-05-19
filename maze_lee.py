#!/bin/env python
import sys
import json
import copy
import math
import argparse
import numpy as np


# IO Utils
def read_input():
    data = json.load(sys.stdin)
    return data["grid"], data["src_coor"], data["dest_coor"]

def write_output( path_exists,  path_length, path_coor):
    json.dump({
        "path_exists": path_exists,
        "path_length": path_length,
        "path_coor"  : path_coor
    }, sys.stdout)

def get_neighbors(grid, visited, values, src , n , m , parents):
    adjacent = []
    if ( src[1] > 0 and src[1] < (n-1) ):
        if ( grid[src[0]][src[1] -1 ][src[2]] != 1  and visited[src[0]][src[1] -1 ][src[2]] == False ):

            adjacent.append([src[0], src[1]-1 , src[2]])
            values[src[0]][src[1]-1][src[2]]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]-1][src[2]] = src

        if ( grid[src[0]][src[1]+1][src[2]] != 1 and visited[src[0]][src[1] +1][src[2]] == False):

            adjacent.append([src[0], src[1]+1 , src[2]])
            values[src[0]][src[1]+1][src[2]]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]+1][src[2]] = src

    elif ( src[1] == 0 ):
        if ( grid[src[0]][src[1]+1][src[2]] != 1 and visited[src[0]][src[1] +1][src[2]] == False):

            adjacent.append([src[0], src[1]+1 , src[2]])
            values[src[0]][src[1]+1][src[2]]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]+1][src[2]] = src
    else:
        if ( grid[src[0]][src[1] -1 ][src[2]] != 1  and visited[src[0]][src[1] -1 ][src[2]] == False ):

            adjacent.append([src[0], src[1]-1 , src[2]])
            values[src[0]][src[1]-1][src[2]]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]-1][src[2]] = src

    if(src[2] > 0 and src[2] < (m-1)) :

        if ( grid[src[0]][src[1]][src[2]-1] != 1  and visited[src[0]][src[1]][src[2] -1] == False ):

            adjacent.append([src[0], src[1] , src[2]-1])
            values[src[0]][src[1]][src[2] -1]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]][src[2] -1] = src

        if ( grid[src[0]][src[1]][src[2]+1] != 1 and visited[src[0]][src[1]][src[2]+1] == False):

            adjacent.append([src[0], src[1] , src[2]+1])
            values[src[0]][src[1]][src[2] +1]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]][src[2] +1] = src

    elif ( src[2] == 0 ):

        if ( grid[src[0]][src[1]][src[2]+1] != 1 and visited[src[0]][src[1]][src[2]+1] == False):
            adjacent.append([src[0], src[1] , src[2]+1])
            values[src[0]][src[1]][src[2] +1]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]][src[2] +1] = src

    else:
        if ( grid[src[0]][src[1]][src[2]-1] == 0  and visited[src[0]][src[1]][src[2] -1] == False ):

            adjacent.append([src[0], src[1] , src[2]-1])
            values[src[0]][src[1]][src[2] -1]  = values[src[0]][src[1]][src[2]] + 1
            parents[src[0]][src[1]][src[2] -1] = src

    if (grid[src[0]][src[1]][src[2]] == 2):
        if (src[0] == 0):

            if(grid[1][src[1]][src[2]] != 1 and visited[1][src[1]][src[2]] == False ):
                adjacent.append([1, src[1] , src[2]])
                values[1][src[1]][src[2]]  = values[src[0]][src[1]][src[2]] + 1
                parents[1][src[1]][src[2]] = src
        else:

            if(grid[0][src[1]][src[2]] != 1 and visited[0][src[1]][src[2]] == False ):
                adjacent.append([0, src[1] , src[2]])
                values[0][src[1]][src[2]]  = values[src[0]][src[1]][src[2]] + 1
                parents[0][src[1]][src[2]] = src

    return adjacent

# Routing
def solve_routing(grid, src_coor, dest_coor):

    destinations = copy.deepcopy(dest_coor)
    # to keep the output
    path_exists = [ False for i in range(len(dest_coor))]
    path_length = [0 for i in range(len(dest_coor))]
    path_coor   = [ [] for i in range(len(dest_coor))]

    d = len(grid)
    n = len(grid[0])
    m = len(grid[0][0])
    queue       = []
    parents = [[[[] for i in range(m)] for j in range(n)] for k in range(d)]
    visited     = [[[False for i in range(m)] for j in range(n)] for k in range(d)]              # indicate the cell is visited or not
    values      = [[[-1 for i in range(m)] for j in range(n)] for k in range(d)]                 # here we set the values of each grid cell

    queue.append(src_coor )                                                                      # push the src in the queue
    values[src_coor[0]][src_coor[1]][src_coor[2]]  = 0                                           # make the src cell visited
    parents[src_coor[0]][src_coor[1]][src_coor[2]] = [-1,-1,-1]

    while(len(queue) != 0):
        src = queue.pop(0)
        visited[src[0]][src[1]][src[2]] = True
        if (src in destinations) :
            path_length[dest_coor.index(src)] = values[0][src[1]][src[2]] + 1
            path_exists[dest_coor.index(src)] = True
            destinations.remove(src)
        if ( len(destinations) == 0):
            break

        neighbors = get_neighbors(grid, visited, values, src, n , m, parents)
        for neighbor in neighbors:
            queue.append(neighbor)

    for i in range(len(path_exists)):
        if path_exists[i]:
            parent = dest_coor[i]
            while (parent != [-1, -1,-1]):
                path_coor[i].append(parent)
                parent = parents[parent[0]][parent[1]][parent[2]]
            path_coor[i].reverse()

    return  path_length , path_exists , path_coor


if __name__ == "__main__":

    grid, src_coor, dest_coor = read_input()

    assert len(grid) in (1, 2), \
        f'expected number of layers to be 1 or 2, found {grid.shape[0]}'

    path_length, path_exists, path_coor = solve_routing( grid, src_coor, dest_coor )
    write_output(path_exists, path_length, path_coor)