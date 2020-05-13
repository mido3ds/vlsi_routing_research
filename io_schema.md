# IO JSON Schema

## General Notation
- H : grid height.
- W : grid width.
- D : number of grid layers (1 or 2).
- N : number of destination cells.
- L : length of specific path (variable).

## Input Schema
Example:

```json
{
    "grid"      : [[[0,0,0],[0,1,0],[0,2,0]],[[1,0,0],[0,1,0],[0,2,1]]],
    "src_coor"  : [0,0,0],
    "dest_coor" : [[1,0,1],[0,2,2]]
}
```

### General Variable Description
- `grid` : An array with depth of 1 (single layer) or 2 (multiple layer) that represents the layout of the chip. Consists of a number of cells, each of which contains the value of 0 (in case of empty cell) or 1 (in case of occupied cell) or 2 (in case of VIA).
- `src_coor` : The coordinates of the source cell in the given grid.
- `dest_coor` : The coordinates of the destination cells in the given grid.

### Variable Dimensions

| Variable     | Type           | Dimensions |
|--------------|----------------|------------|
| grid         | Integer(0,1,2) | D x H x W  |
| src_coor     | Integer        | 3          |
| dest_coor    | Integer        | N x 3      |

## Output Schema
Example:

```json
{
    "path_exists" : [true,true],
    "path_length" : [4,5],
    "path_coor"   : [[[0,1,0],[1,1,1],[1,1,2],[1,2,2]],[[0,1,0],[0,1,1],[1,1,1],[1,1,2],[1,1,3]]]
}
```

### General Variable Description
- `path_exists` : An array of booleans defining whether a path is found between source and destination.
- `path_length` : An array of integers defining the number of cells along each path.
- `path_coor` : An array of arrays defining the coordinates of of the cells along each path.

### Variable Dimensions

| Variable     | Type         | Dimensions |
|--------------|--------------|------------|
| path_exists  | Boolean      | N          |
| path_length  | Integer      | N          |
| path_coor    | Integer      | N x L x 3  |
