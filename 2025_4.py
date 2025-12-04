import aocd

import cli

from vector import Vector

sample_data = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
data = sample_data if cli.sample else aocd.data


class Room:
    def __init__(self, layout):
        self.layout = layout.splitlines()
        self.height = len(self.layout)
        self.width = len(self.layout[0])

    def __getitem__(self, x):
        class Proxy:
            def __init__(self, my_room, x):
                self._my_room = my_room
                self._x = x

            def __getitem__(self, y):
                if y < 0 or y >= self._my_room.height:
                    return None
                if x < 0 or x >= self._my_room.width:
                    return None
                return self._my_room.layout[y][self._x]

        return Proxy(self, x)


room = Room(data)
positions = [Vector(x, y) for y in range(room.height) for x in range(room.width)]
paper_positions = [p for p in positions if room[p.x][p.y] == "@"]

paper_neighbours = [
    [n for n in p.neighbours() if room[n.x][n.y] == "@"] for p in paper_positions
]
num_paper_neighbours = [len(n) for n in paper_neighbours]
valid_positions = [p for (p, n) in zip(paper_positions, num_paper_neighbours) if n < 4]

print(f"Problem 1: {len(valid_positions)}")
