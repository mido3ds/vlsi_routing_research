#!/bin/env python3
import json
import sys
from typing import NamedTuple, List

import numpy as np

_print = print
print = lambda *args, **kwargs: _print(*args, **kwargs, file=sys.stderr)


class Point(NamedTuple):
    d: int
    h: int
    w: int

    def dist(self, b) -> int:
        # ignores the `d`
        return abs(self.h - b.h) + abs(self.w - b.w)

    def tolist(self) -> List[int]:
        return [self.d, self.h, self.w]


class Line(NamedTuple):
    a: Point
    b: Point


class Path(NamedTuple):
    points: List[Point]

    def len(self) -> int:
        s = 0
        for i in range(len(self.points)-1):
            s += self.points[i].dist(self.points[i+1])
        return s


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
        out['path_coor'].append([x.tolist() for x in path.points])

    json.dump(out, sys.stdout)
