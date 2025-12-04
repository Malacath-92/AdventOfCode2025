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
        self.layout = [list(l) for l in layout.splitlines()]
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

            def __setitem__(self, y, item):
                if y < 0 or y >= self._my_room.height:
                    return
                if x < 0 or x >= self._my_room.width:
                    return
                self._my_room.layout[y][self._x] = item

        return Proxy(self, x)


room = Room(data)
positions = [Vector(x, y) for y in range(room.height) for x in range(room.width)]
paper_positions = [p for p in positions if room[p.x][p.y] == "@"]
num_paper_neighbours = {
    p: len([n for n in p.neighbours() if room[n.x][n.y] == "@"])
    for p in paper_positions
}


def get_accessible_positions():
    return [p for p in paper_positions if num_paper_neighbours[p] < 4]


accessible_positions = get_accessible_positions()
print(f"Problem 1: {len(accessible_positions)}")

total_removed = 0
while accessible_positions:
    total_removed += len(accessible_positions)
    for p in accessible_positions:
        room[p.x][p.y] = " "

        paper_positions.remove(p)
        num_paper_neighbours.pop(p)
        for n in p.neighbours():
            if n in num_paper_neighbours:
                num_paper_neighbours[n] -= 1
    accessible_positions = get_accessible_positions()
print(f"Problem 1: {total_removed}")
