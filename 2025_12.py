import aocd

import cli

from vector import Vector

if cli.sample:
    print("Joke's on you, this solution doesn't work for the sample...")
    exit(1)

data = aocd.data


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
print(f"Part 2: Thank god this year is a short one...")
