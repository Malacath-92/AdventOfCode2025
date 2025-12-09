import aocd

import cli

from vector import Vector

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

tiles = [Vector(*map(int, line.split(","))) for line in data.splitlines()]

square_corners = list(combinations(tiles, r=2))
square_diagonals = [lhs - rhs for lhs, rhs in square_corners]
square_areas = [(abs(diag.x) + 1) * (abs(diag.y) + 1) for diag in square_diagonals]

print("Part 1:", max(square_areas))
