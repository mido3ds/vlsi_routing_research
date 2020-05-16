#!/bin/env python3
import json
import sys
from typing import NamedTuple, List, Generator, Union

import numpy as np

_print = print
print = lambda *args, **kwargs: _print(*args, **kwargs, file=sys.stderr)

# cell type
OBSTACLE = 0
VIA = 1
SRC = 2
DEST = 3


def is_cell(v: int, cell_type: int) -> bool:
    # i.e. is_cell(2, VIA) => True
    return (v >> cell_type) & 1 == 1


def is_src_on_dest(v: int) -> bool:
    return (v >> SRC) & 0b11 == 0b11


def put_cell(v: int, cell_type: int) -> int:
    # i.e. put_cell(0, SRC) => 4
    return v | 1 << cell_type


class Point(NamedTuple):
    d: int
    h: int
    w: int

    def dist(self, b) -> int:
        # ignores the `d`
        return abs(self.h - b.h) + abs(self.w - b.w)

    def _replace_i(self, i: int, value: int):
        l = list(self)
        l[i] = value
        return Point._make(l)

    def __eq__(self, a) -> bool:
        for i in range(3):
            if self[i] != a[i]:
                return False
        return True


class Line(NamedTuple):
    a: Point
    b: Point

    def is_vertical(self) -> bool:
        return self.a.d == self.b.d and self.a.w == self.b.w

    def dim(self) -> int:
        assert self.a != self.b, 'not line'

        for i in range(3):
            if self.a[i] != self.b[i]:
                return i

    def points(self, inclusive=True):
        dim = self.dim()

        step = 1 if self.b[dim] >= self.a[dim] else -1
        a = self.a[dim] if inclusive else self.a[dim]+step
        b = self.b[dim]+step if inclusive else self.b[dim]

        for x in range(a, b, step):
            yield self.a._replace_i(dim, x)

    def intersection(self, l2) -> Point:
        sv, l2v = self.is_vertical(), l2.is_vertical()
        assert (sv and not l2v) or (not sv and l2v),\
            f'lines {self}, {l2} must be one vertical and the other horizontal, not both'

        x, y = (self, l2) if sv else (l2, self)

        assert x.a.h <= y.a.h and x.b.h >= y.b.h and y.a.w <= x.a.w and y.b.w >= x.b.w,\
            f'lines {x},{y} are not intersecting'

        return Point(d=l2.a.d, w=x.a.w, h=y.a.h)

    def __contains__(self, c):
        return c.d == self.a.d and \
            ((c.h == self.a.h == self.b.h) or (c.w == self.a.w == self.b.w))


class Path(NamedTuple):
    points: List[Point]

    def len(self) -> int:
        s = 0
        for i in range(len(self.points)-1):
            s += self.points[i].dist(self.points[i+1])
        return s


def add_line(grid: np.ndarray, p: Point, cell_type: int, dim: int) -> Line:
    assert dim in (1, 2), 'dim should be either 1 or 2'

    grid[p] = put_cell(grid[p], cell_type)

    max_x = p[dim]
    min_x = p[dim]

    # possible lines
    lines = [
        #     p -->
        Line(p, p._replace_i(dim, grid.shape[dim])),
        # <-- p
        Line(p, p._replace_i(dim, -1))
    ]

    for line in lines:
        for p2 in line.points(inclusive=False):
            # TODO: extend over vias with recursion
            if is_cell(grid[p2], OBSTACLE):
                break

            max_x = p2[dim]
            grid[p2] = put_cell(grid[p2], cell_type)

    return Line(p._replace_i(dim, min_x), p._replace_i(dim, max_x))


def solve_one_target(grid: np.ndarray, src_coor: Point, dest_coor: Point, src_levels: List[List[Line]]) -> Path:
    # # levels[0] = src_levels, levels[1] = dest_levels
    # levels = [src_levels, []]

    # # start with vert+hor lines for target
    # # each line has T as parent backtracking point
    # levels[1].append(horizontal_line(...))
    # levels[1].append(vertical_line(...))

    # # while no new craeted lines for both S and T:
    # while len(levels[0][-1]) != 0 and len(levels[0][-1]) != 0
    #   for i in (0,1):
    #       # create new level
    #       levels[i].append([])

    #       # for each line l0 in previous level:
    #       for l0 in levels[i][-2]:
    #           # for each point on line:
    #           for p in l0.points():
    #               # create perpend line l1, where its parent is l0

    #               # if crossed point:
    #                   # search for its line L3
    #                   # bactrack l1 to S and L3 to T (or vice versa)
    #                   # create path of backtracking points
    #                   # clean grid of dest
    #                   return path
    # # clean grid of dest
    # return Path([])

    # TODO
    return Path([Point(5, 6, 7), Point(1, 2, 3)])


def solve(grid: np.ndarray, src_coor: Point, dest_coor: List[Point]) -> List[Path]:
    # TODO
    # start with vert+hor lines for src
    # each line has S as parent backtracking point

    src_levels: List[List[Line]] = []

    return [solve_one_target(grid, src_coor, dest, src_levels) for dest in dest_coor]


if __name__ == "__main__":
    # read
    inp = json.load(sys.stdin)

    grid = np.array(inp['grid'], dtype='uint8')
    src_coor = Point._make(inp['src_coor'])
    dest_coor = [Point._make(x) for x in inp['dest_coor']]

    # solve
    paths = solve(grid, src_coor, dest_coor)

    # write
    out = {
        "path_exists": [],
        "path_length": [],
        "path_coor": []
    }

    for path in paths:
        out['path_exists'].append(len(path.points) != 0)
        out['path_length'].append(path.len())
        out['path_coor'].append([list(x) for x in path.points])

    json.dump(out, sys.stdout)
