import aocd

import cli

from vector import Vector2
from sliding_window import sliding_window

from itertools import combinations

sample_data = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
data = sample_data if cli.sample else aocd.data

tiles = [Vector2(*map(int, line.split(","))) for line in data.splitlines()]


class Line:
    def __init__(self, start: Vector2, end: Vector2):
        self.start = start
        self.end = end


class Box:
    def __init__(self, lhs_corner: Vector2, rhs_corner: Vector2):
        min_corner = Vector2(
            min(lhs_corner.x, rhs_corner.x),
            min(lhs_corner.y, rhs_corner.y),
        )
        max_corner = Vector2(
            max(lhs_corner.x, rhs_corner.x),
            max(lhs_corner.y, rhs_corner.y),
        )
        self.min = min_corner
        self.max = max_corner
        self.delta = max_corner - min_corner

    @property
    def area(self):
        return (abs(self.delta.x) + 1) * (abs(self.delta.y) + 1)

    def intersects(self, line: Line):
        # Only axis-aligned lines
        assert line.start.x == line.end.x or line.start.y == line.end.y

        if line.start.x == line.end.x:
            line_x = line.start.x
            line_min_y = min(line.start.y, line.end.y)
            line_max_y = max(line.start.y, line.end.y)

            return (
                self.min.x < line_x < self.max.x
                and line_max_y > self.min.y
                and line_min_y < self.max.y
            )
        else:
            line_y = line.start.y
            line_min_x = min(line.start.x, line.end.x)
            line_max_x = max(line.start.x, line.end.x)

            return (
                self.min.y < line_y < self.max.y
                and line_max_x > self.min.x
                and line_min_x < self.max.x
            )


square_corners = list(combinations(tiles, r=2))
boxes = [Box(lhs, rhs) for lhs, rhs in square_corners]
boxes_sorted = sorted(boxes, key=lambda box: box.area, reverse=True)

print(f"Part 1: {boxes_sorted[0].area}")

lines = list(Line(lhs, rhs) for lhs, rhs in sliding_window(tiles, 2)) + [
    Line(tiles[-1], tiles[0])
]

for box in boxes_sorted:
    if not any(box.intersects(line) for line in lines):
        print(f"Part 2: {box.area}")
        break
