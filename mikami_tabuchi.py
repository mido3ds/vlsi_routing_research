#!/bin/env python3
from __future__ import annotations

import json
import sys
from typing import Generator, List, NamedTuple, Union, Optional

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


def dest_to_src(grid: np.ndarray) -> np.ndarray:
    grid &= np.array(~(1 << DEST), dtype=grid.dtype)
    return grid


class Point(NamedTuple):
    d: int
    h: int
    w: int

    def _replace_i(self, i: int, value: int) -> Point:
        l = list(self)
        l[i] = value
        return Point._make(l)

    def __repr__(self):
        return f'p({self.d},{self.h},{self.w})'


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

    def perpend_dim(self) -> int:
        '''
        return dim of line perpendicular to this
        1 -> 2
        2 -> 1
        '''
        if self.dim() == 1:
            return 2

        return 1

    def points(self, inclusive=True):
        dim = self.dim()

        step = 1 if self.b[dim] >= self.a[dim] else -1
        a = self.a[dim] if inclusive else self.a[dim]+step
        b = self.b[dim]+step if inclusive else self.b[dim]

        for x in range(a, b, step):
            yield self.a._replace_i(dim, x)

    def intersection(self, l2: Line) -> Point:
        assert self.intersects(l2), f'lines {self},{l2} are not intersecting'

        # me is a point
        if self.a == self.b and self.a in l2:
            return self.a

        # other is a point
        if l2.a == l2.b and l2.a in self:
            return l2.a

        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#given_two_points_on_each_line
        x1, x2, x3, x4 = self.a.h, self.b.h, l2.a.h, l2.b.h
        y1, y2, y3, y4 = self.a.w, self.b.w, l2.a.w, l2.b.w

        deno = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)

        assert deno != 0, f'lines {self},{l2} are parallel'

        t = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        t /= deno
        if t >= 0 and t <= 1:
            return Point(d=self.a.d, h=int(x1+t*(x2-x1)), w=int(y1+t*(y2-y1)))

        u = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
        u /= -deno
        if u >= 0 and u <= 1:
            return Point(d=self.a.d, h=int(x3+u*(x4-x3)), w=int(y3+u*(y4-y3)))

        raise AssertionError(f'lines {self},{l2} are not intersecting')

    def intersects(self, l2: Line) -> bool:
        if self == l2:
            return True

        def orientation(p, q, r):
            '''
            to find the orientation of an ordered triplet (p,q,r)
            See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
            '''
            val = (float(q.w - p.w) * (r.h - q.h)) - \
                (float(q.h - p.h) * (r.w - q.w))

            if val > 0:
                # clockwise orientation
                return 1
            elif val < 0:
                # counterclockwise orientation
                return 2

            # colinear orientation
            return 0

        def pts_on_segment(p, q, r):
            '''
            Given three colinear points p, q, r, the function checks if
            point q lies on line segment 'pr'
            '''
            return ((q.h <= max(p.h, r.h)) and (q.h >= min(p.h, r.h)) and
                    (q.w <= max(p.w, r.w)) and (q.w >= min(p.w, r.w)))

        x1, y1, x2, y2 = self.a, self.b, l2.a, l2.b

        # find the 4 orientations required for
        # the general and special cases
        o1 = orientation(x1, y1, x2)
        o2 = orientation(x1, y1, y2)
        o3 = orientation(x2, y2, x1)
        o4 = orientation(x2, y2, y1)

        # general case
        if (o1 != o2) and (o3 != o4):
            return True

        # special Cases

        # x1 , y1 and x2 are colinear and x2 lies on segment p1q1
        if (o1 == 0) and pts_on_segment(x1, x2, y1):
            return True

        # x1 , y1 and y2 are colinear and y2 lies on segment p1q1
        if (o2 == 0) and pts_on_segment(x1, y2, y1):
            return True

        # x2 , y2 and x1 are colinear and x1 lies on segment p2q2
        if (o3 == 0) and pts_on_segment(x2, x1, y2):
            return True

        # x2 , y2 and y1 are colinear and y1 lies on segment p2q2
        if (o4 == 0) and pts_on_segment(x2, y1, y2):
            return True

        # if none of the cases
        return False

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

    def __repr__(self):
        return f'l({self.a}->{self.b}~{self.p})'


Path = List[Point]


def intersect_lines(lines: List[Line]) -> Path:
    path: Path = []
    # print('intersect_lines', lines)
    for i in range(len(lines)-1):
        path.append(lines[i].intersection(lines[i+1]))
    return path


def build_path(a: Line, b: Line) -> Path:
    # src --> a . b --> dst

    src, a_to_src = a.backtrack()
    src_to_a = list(reversed(a_to_src))

    dst, b_to_dst = b.backtrack()

    return [src] + intersect_lines(src_to_a + b_to_dst) + [dst]


def add_lines(grid: np.ndarray, p0: Point, cell_type: int, dim: int, parent: Union[Point, Line], enable_recursion=True) -> (List[Line], bool):
    assert dim in (1, 2), 'dim should be either 1 or 2'
    assert not is_cell(grid[p0], OBSTACLE), 'started line with obstacle point'

    lines = []
    max_x = p0[dim]
    min_x = p0[dim]

    def new_line():
        return Line(p0._replace_i(dim, min_x), p0._replace_i(dim, max_x), parent)

    # 2 possible directions
    points_set = [
        # points in [..., p0]
        Line(p0, p0._replace_i(dim, 0), None).points(True),
        # points in (p0,...]
        Line(p0, p0._replace_i(dim, grid.shape[dim]), None).points(False)
    ]

    for points in points_set:
        for p1 in points:
            if is_cell(grid[p1], OBSTACLE):
                break

            if enable_recursion and is_cell(grid[p1], VIA):
                new_lines, crossed = add_lines(
                    grid,
                    p1._replace(d=1-p1.d),
                    cell_type, dim, new_line(), enable_recursion=False
                )

                if crossed:
                    return new_lines, True
                else:
                    lines += new_lines

            max_x = p1[dim]
            grid[p1] = put_cell(grid[p1], cell_type)

            if is_src_on_dest(grid[p1]):
                return [new_line()], True

    if min_x == max_x:
        return lines, False

    return lines + [new_line()], False


def search_in_levels(l: Line, levels: List[List[Line]]) -> Optional[Line]:
    for level in levels:
        for l2 in level:
            if l.intersects(l2):
                return l2


def remove_duplicates(l: List[object]) -> List[object]:
    if len(l) == 0:
        return l
    l2 = [l[0]]
    for el in l[1:]:
        if l2[-1] != el:
            l2.append(el)
    return l2


def solve_one_target(grid: np.ndarray, src_coor: Point, dest_coor: Point, src_levels: List[List[Line]]) -> Path:
    # levels[0] = src_levels, levels[1] = dest_levels
    levels = [src_levels, [[]]]

    # start with vert+hor lines for target
    # each line has T as parent backtracking point
    levels[1][0] += add_lines(grid, dest_coor, DEST, 1, dest_coor)[0]
    levels[1][0] += add_lines(grid, dest_coor, DEST, 2, dest_coor)[0]

    # while no new craeted lines for both S and T:
    while len(levels[0][-1]) != 0 and len(levels[0][-1]) != 0:
        for i, cell_type in enumerate((SRC, DEST)):
            # create new level
            levels[i].append([])

            # for each line l0 in previous level:
            for l0 in levels[i][-2]:
                # for each point on line:
                for p in l0.points():
                    # create perp_l0, where its parent is l0
                    perp_l0, crossed = add_lines(
                        grid, p, cell_type, l0.perpend_dim(), l0
                    )
                    print(grid)
                    levels[i][-1] += perp_l0

                    if crossed:
                        # search for its line l3 in the other level
                        l3 = search_in_levels(perp_l0[0], levels[1-i])
                        assert l3 is not None, f'line={perp_l0[0]} doesnt intersect with any line in levels={levels[1-i]}, i={i}'

                        # bactrack perp_l0 to S and l3 to T (or vice versa) and create path of backtracking points
                        a, b = (perp_l0[0], l3) if i == 0 else (l3, perp_l0[0])
                        path = build_path(a, b)

                        # clean grid of dest
                        grid = dest_to_src(grid)
                        print(path)
                        return remove_duplicates(path)

    # clean grid of dest
    grid = dest_to_src(grid)
    return []


def solve(grid: np.ndarray, src_coor: Point, dest_coor: List[Point]) -> List[Path]:
    src_levels: List[List[Line]] = [[]]

    # start with vert+hor lines for src
    # each line has S as parent backtracking point
    src_levels[0] += add_lines(grid, src_coor, SRC, 1, src_coor)[0]
    src_levels[0] += add_lines(grid, src_coor, SRC, 2, src_coor)[0]

    return [solve_one_target(grid, src_coor, dest, src_levels) for dest in dest_coor]


if __name__ == "__main__":
    # read
    inp = json.load(sys.stdin)

    grid = np.array(inp['grid'], dtype='uint8')
    src_coor = Point._make(inp['src_coor'])
    dest_coor = [Point._make(x) for x in inp['dest_coor']]

    # for tests TODO
    grid[:] = 0

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
