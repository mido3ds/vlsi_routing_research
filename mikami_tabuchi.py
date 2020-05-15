#!/bin/env python3
import json
import sys
from typing import NamedTuple, List, Generator

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


class Line(NamedTuple):
    a: Point
    b: Point

    def is_vertical(self) -> bool:
        return self.a.d == self.b.d and self.a.w == self.b.w

    def points(self):
        if self.is_vertical():
            for h in range(self.a.h, self.b.h+1):
                yield self.a._replace(h=h)
        else:
            for w in range(self.a.w, self.b.w+1):
                yield self.a._replace(w=w)

    def intersection(self, l2) -> Point:
        sv, l2v = self.is_vertical(), l2.is_vertical()
        assert (sv and not l2v) or (not sv and l2v),\
            f'lines {self}, {l2} must be one vertical and the other horizontal, not both'

        x, y = (self, l2) if sv else (l2, self)

        assert x.a.h <= y.a.h and x.b.h >= y.b.h and y.a.w <= x.a.w and y.b.w >= x.b.w,\
            f'lines {x},{y} are not intersecting'

        return Point(d=l2.a.d, w=x.a.w, h=y.a.h)


class Path(NamedTuple):
    points: List[Point]

    def len(self) -> int:
        s = 0
        for i in range(len(self.points)-1):
            s += self.points[i].dist(self.points[i+1])
        return s


def horizontal_line(grid: np.ndarray, p: Point, cell_type: int) -> (Line, np.ndarray):
    max_w = p.w
    min_w = p.w

    for w in range(p.w, grid.shape[2]):
        if is_cell(grid[p.d, p.h, w], OBSTACLE):
            break

        max_w = w
        grid[p.d, p.h, w] = put_cell(grid[p.d, p.h, w], cell_type)

    for w in range(p.w, 0, -1):
        if is_cell(grid[p.d, p.h, w], OBSTACLE):
            break

        min_w = w
        grid[p.d, p.h, w] = put_cell(grid[p.d, p.h, w], cell_type)

    return Line(p._replace(w=min_w), p._replace(w=max_w)), grid


def vertical_line(grid: np.ndarray, p: Point, cell_type: int) -> (Line, np.ndarray):
    max_h = p.h
    min_h = p.h

    for h in range(p.h, grid.shape[1]):
        if is_cell(grid[p.d, h, p.w], OBSTACLE):
            break

        max_h = h
        grid[p.d, h, p.w] = put_cell(grid[p.d, h, p.w], cell_type)

    for h in range(p.h, 0, -1):
        if is_cell(grid[p.d, h, p.w], OBSTACLE):
            break

        min_h = h
        grid[p.d, h, p.w] = put_cell(grid[p.d, h, p.w], cell_type)

    return Line(p._replace(h=min_h), p._replace(h=max_h)), grid


def solve(grid, src_coor, dest_coor) -> List[Path]:
    # TODO
    return [Path([Point(5, 6, 7), Point(1, 2, 3)])] * len(dest_coor)


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
