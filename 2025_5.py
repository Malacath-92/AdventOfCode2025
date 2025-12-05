import aocd

import cli

from vector import Vector

sample_data = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
data = sample_data if cli.sample else aocd.data

records = data.split("\n\n")
fresh_ranges = [list(map(int, line.split("-"))) for line in records[0].splitlines()]
available = [int(line) for line in records[1].splitlines()]

def is_fresh(ingredient):
    for min, max in fresh_ranges:
        if min <= ingredient <= max:
            return True
    return False

fresh_ingredients = [ingredient for ingredient in available if is_fresh(ingredient)]

print("Problem 1:", len(fresh_ingredients))