#!/bin/env python3
from __future__ import annotations

import json
import sys
from typing import Generator, List, NamedTuple, Union

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
    return v & (1 << cell_type) != 0


def is_src_on_dest(v: int) -> bool:
    return (v >> SRC) & 0b11 == 0b11


def put_cell(v: int, cell_type: int) -> int:
    # i.e. put_cell(0, SRC) => 4
    return v | (1 << cell_type)


def remove_dest(grid: np.ndarray) -> np.ndarray:
    return np.bitwise_and(grid, np.array(~(1 << DEST), dtype=grid.dtype), out=grid)


class Point(NamedTuple):
    d: int
    h: int
    w: int

    def dist(self, b: Point) -> int:
        # ignores the `d`
        return abs(self.h - b.h) + abs(self.w - b.w)

    def _replace_i(self, i: int, value: int):
        l = list(self)
        l[i] = value
        return Point._make(l)

    def __eq__(self, a: Point) -> bool:
        for i in range(3):
            if self[i] != a[i]:
                return False
        return True


class Line(NamedTuple):
    a: Point
    b: Point

    # parent of this line
    p: Union[Point, Line]

    def is_vertical(self) -> bool:
        return self.a.d == self.b.d and self.a.w == self.b.w

    def dim(self) -> int:
        for i in range(3):
            if self.a[i] != self.b[i]:
                return i
        return 1

    def points(self, inclusive=True):
        dim = self.dim()

        step = 1 if self.b[dim] >= self.a[dim] else -1
        a = self.a[dim] if inclusive else self.a[dim]+step
        b = self.b[dim]+step if inclusive else self.b[dim]

        for x in range(a, b, step):
            yield self.a._replace_i(dim, x)

    def intersection(self, l2: Line) -> Point:
        sv, l2v = self.is_vertical(), l2.is_vertical()
        assert (sv and not l2v) or (not sv and l2v),\
            f'lines {self}, {l2} must be one vertical and the other horizontal, not both'

        x, y = (self, l2) if sv else (l2, self)

        assert x.a.h <= y.a.h and x.b.h >= y.b.h and y.a.w <= x.a.w and y.b.w >= x.b.w,\
            f'lines {x},{y} are not intersecting'

        return Point(d=l2.a.d, w=x.a.w, h=y.a.h)

    def __contains__(self, c: Point):
        return c.d == self.a.d and \
            ((c.h == self.a.h == self.b.h) or (c.w == self.a.w == self.b.w))

    def backtrack(self) -> (Point, List[Line]):
        lines = [self]
        parent = self.p
        assert parent is not None

        while type(parent) != Point:
            lines.append(parent)
            parent = parent.p

            assert parent is not None

        return parent, lines


Path = List[Point]


def intersect_lines(lines: List[Line]) -> Path:
    path: Path = []
    for i in range(len(lines)-1):
        path.append(lines[i].intersection(lines[i+1]))
    return path


def build_path(a: Line, b: Line) -> Path:
    # src --> a . b --> dst

    src, a_to_src = a.backtrack()
    src_to_a = list(reversed(a_to_src))

    dst, b_to_dst = b.backtrack()

    return [src] + intersect_lines(src_to_a + b_to_dst) + [dst]


def add_lines(grid: np.ndarray, p0: Point, cell_type: int, dim: int, enable_recursion=True) -> List[Line]:
    assert dim in (1, 2), 'dim should be either 1 or 2'
    assert not is_cell(grid[p0], OBSTACLE), 'started line with obstacle point'

    lines = []
    max_x = p0[dim]
    min_x = p0[dim]

    # 2 possible directions
    points_set = [
        # points in [..., p0]
        Line(p0, p0._replace_i(dim, 0)).points(inclusive=True),
        # points in (p0,...]
        Line(p0, p0._replace_i(dim, grid.shape[dim])).points(inclusive=False)
    ]

    for points in points_set:
        for p1 in points:
            if is_cell(grid[p1], OBSTACLE):
                break

            if enable_recursion and is_cell(grid[p1], VIA):
                lines += add_lines(
                    grid,
                    p1._replace(d=1-p1.d),
                    cell_type, dim, enable_recursion=False
                )

            max_x = p1[dim]
            grid[p1] = put_cell(grid[p1], cell_type)

    return lines + [Line(p0._replace_i(dim, min_x), p0._replace_i(dim, max_x))]


def solve_one_target(grid: np.ndarray, src_coor: Point, dest_coor: Point, src_levels: List[List[Line]]) -> Path:
    # # levels[0] = src_levels, levels[1] = dest_levels
    # levels = [src_levels, []]

    # # start with vert+hor lines for target
    # # each line has T as parent backtracking point
    # levels[1].append(add_lines(grid, dest_coor, DEST, 1))
    # levels[1].append(add_lines(grid, dest_coor, DEST, 2))

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
    #                   grid = remove_dest(grid)
    #                   return path
    # # clean grid of dest
    # grid = remove_dest(grid)
    # return []

    # TODO
    return [Point(5, 6, 7), Point(1, 2, 3)]


def solve(grid: np.ndarray, src_coor: Point, dest_coor: List[Point]) -> List[Path]:
    # TODO
    # start with vert+hor lines for src
    # each line has S as parent backtracking point
    # levels[1].append(add_lines(grid, src_coor, SRC, 1))
    # levels[1].append(add_lines(grid, src_coor, SRC, 2))

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
        out['path_exists'].append(len(path) != 0)
        out['path_length'].append(len(path))
        out['path_coor'].append([list(x) for x in path])

    json.dump(out, sys.stdout)
