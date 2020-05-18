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

def write_output( path_exists,  path_length):
    json.dump({
        "path_exists": path_exists,
        "path_length": path_length
        #"path_coor": path_coor
    }, sys.stdout)

def get_neighbors(grid, visited, values, src , n , m ):
    adjacent = []
    if ( src[1] > 0 and src[1] < (n-1) ):
        if ( grid[src[0]][src[1] -1 ][src[2]] != 1  and visited[src[0]][src[1] -1 ][src[2]] == False ):

            adjacent.append([src[0], src[1]-1 , src[2]])
            values[src[0]][src[1]-1][src[2]] = values[src[0]][src[1]][src[2]] + 1

        if ( grid[src[0]][src[1]+1][src[2]] != 1 and visited[src[0]][src[1] +1][src[2]] == False):

            adjacent.append([src[0], src[1]+1 , src[2]])
            values[src[0]][src[1]+1][src[2]] = values[src[0]][src[1]][src[2]] + 1

    elif ( src[1] == 0 ):
        if ( grid[src[0]][src[1]+1][src[2]] != 1 and visited[src[0]][src[1] +1][src[2]] == False):

            adjacent.append([src[0], src[1]+1 , src[2]])
            values[src[0]][src[1]+1][src[2]] = values[src[0]][src[1]][src[2]] + 1
    else:
        if ( grid[src[0]][src[1] -1 ][src[2]] != 1  and visited[src[0]][src[1] -1 ][src[2]] == False ):

            adjacent.append([src[0], src[1]-1 , src[2]])
            values[src[0]][src[1]-1][src[2]] = values[src[0]][src[1]][src[2]] + 1

    if(src[2] > 0 and src[2] < (m-1)) :

        if ( grid[src[0]][src[1]][src[2]-1] != 1  and visited[src[0]][src[1]][src[2] -1] == False ):

            adjacent.append([src[0], src[1] , src[2]-1])
            values[src[0]][src[1]][src[2] -1] = values[src[0]][src[1]][src[2]] + 1

        if ( grid[src[0]][src[1]][src[2]+1] != 1 and visited[src[0]][src[1]][src[2]+1] == False):

            adjacent.append([src[0], src[1] , src[2]+1])
            values[src[0]][src[1]][src[2] +1] = values[src[0]][src[1]][src[2]] + 1

    elif ( src[2] == 0 ):

        if ( grid[src[0]][src[1]][src[2]+1] != 1 and visited[src[0]][src[1]][src[2]+1] == False):
            adjacent.append([src[0], src[1] , src[2]+1])
            values[src[0]][src[1]][src[2] +1] = values[src[0]][src[1]][src[2]] + 1

    else:
        if ( grid[src[0]][src[1]][src[2]-1] == 0  and visited[src[0]][src[1]][src[2] -1] == False ):

            adjacent.append([src[0], src[1] , src[2]-1])
            values[src[0]][src[1]][src[2] -1] = values[src[0]][src[1]][src[2]] + 1

    if (grid[src[0]][src[1]][src[2]] == 2):
        if (src[0] == 0):

            if(grid[1][src[1]][src[2]] != 1 and visited[1][src[1]][src[2]] == False ):
                adjacent.append([1, src[1] , src[2]])
                values[1][src[1]][src[2]] = values[src[0]][src[1]][src[2]] + 1
        else:

            if(grid[0][src[1]][src[2]] != 1 and visited[0][src[1]][src[2]] == False ):
                adjacent.append([0, src[1] , src[2]])
                values[0][src[1]][src[2]] = values[src[0]][src[1]][src[2]] + 1

    return adjacent

# Routing
def solve_routing(grid, src_coor, dest_coor):

    destinations = copy.deepcopy(dest_coor)
    # to keep the output
    path_exists = [ False for i in range(len(dest_coor))]
    path_length = [0 for i in range(len(dest_coor))]
    #path_coor   = []

    d = len(grid)
    n = len(grid[0])
    m = len(grid[0][0])
    queue       = []
    visited     = [[[False for i in range(m)] for j in range(n)] for k in range(d)]              # indicate the cell is visited or not
    values      = [[[-1 for i in range(m)] for j in range(n)] for k in range(d)]                 # here we set the values of each grid cell

    queue.append(src_coor )                                                                      # push the src in the queue
    values[src_coor[0]][src_coor[1]][src_coor[2]]  = 0                                           # make the src cell visited

    while(len(queue) != 0):
        src = queue.pop(0)
        visited[src[0]][src[1]][src[2]] = True
        if (src in destinations) :
            path_length[dest_coor.index(src)] = values[0][src[1]][src[2]] + 1
            path_exists[dest_coor.index(src)] = True
            destinations.remove(src)
        if ( len(destinations) == 0):
            break

        neighbors = get_neighbors(grid, visited, values, src, n , m)
        for neighbor in neighbors:
            queue.append(neighbor)

    #here we save the coordinates
    # get the max value from all destinations and backtrack until getting the source
    return  path_length , path_exists
    #return path_exists, path_length, path_coor


if __name__ == "__main__":

    grid, src_coor, dest_coor = read_input()

    assert len(grid) in (1, 2), \
        f'expected number of layers to be 1 or 2, found {grid.shape[0]}'

    path_exists, path_length = solve_routing( grid, src_coor, dest_coor )
    write_output(path_exists, path_length)