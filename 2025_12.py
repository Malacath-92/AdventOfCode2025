import aocd

import cli

from vector import Vector

sample_data = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
data = sample_data if cli.sample else aocd.data


class Container:
    def __init__(self, scheme):
        size, presents = scheme.split(":")
        self.size = Vector(*map(int, size.split("x")))
        self.presents = list(map(int, presents.strip().split()))

    # None of the pieces in the real input actually efficiently fit together
    # so we may as well treat them all as 3x3 boxes and see how many fit
    @property
    def simple_fits_presents(self):
        return (self.size.x // 3) * (self.size.y // 3) >= sum(self.presents)


parts = data.split("\n\n")
containers = list(map(Container, parts[-1].splitlines()))

print(f"Part 1: {len(list(c for c in containers if c.simple_fits_presents))}")
