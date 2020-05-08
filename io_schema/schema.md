# IO JSON Schema

## General Notation
- H : grid height.
- W : grid width.
- D : number of grid layers.
- N : number of destination cells.
- L : length of specific path (variable).

## Input Schema

### General Variable Description
- `grid` : An array that represents the layout of the chip. 2D in case of single layer and 3D in case of multiple layers.
Consists of a number of cells, each of which contains the value of 0 (in case of empty cell) or 1 (in case of occupied cell).
- `src_coor` : The coordinates of the source cell in the given grid.
- `dest_coor` : The coordinates of the destination cells in the given grid.

### Single layer Scenario

| Variable     | Type         | Dimensions |
|--------------|--------------|------------|
| grid         | Integer(0,1) | H x W      |
| src_coor     | Integer      | 1 x 2      |
| dest_coor    | Integer      | N x 2      |

### Multi layer Scenario

| Variable     | Type         | Dimensions |
|--------------|--------------|------------|
| grid         | Integer(0,1) | D x H x W  |
| src_coor     | Integer      | 1 x 3      |
| dest_coor    | Integer      | N x 3      |

## Output Schema

### General Variable Description
- `path_exists` : An array of booleans defining whether a path is found between source and destination.
- `path_length` : An array of integers defining the number of cells along each path.
- `path_coor` : An array of arrays defining the coordinates of of the cells along each path.

### Single layer Scenario

| Variable     | Type         | Dimensions |
|--------------|--------------|------------|
| path_exists  | Boolean      | N          |
| path_length  | Integer      | N          |
| path_coor    | Integer      | N x L x 2  |

### Multi layer Scenario

| Variable     | Type         | Dimensions |
|--------------|--------------|------------|
| path_exists  | Boolean      | N          |
| path_length  | Integer      | N          |
| path_coor    | Integer      | N x L x 3  |
