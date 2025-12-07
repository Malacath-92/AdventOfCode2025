import aocd

import cli

from functools import lru_cache

sample_data = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
data = sample_data if cli.sample else aocd.data


class Field:
    def __init__(self, layout):
        self.layout = [list(l) for l in layout.splitlines()]
        self.height = len(self.layout)
        self.width = len(self.layout[0])

    def __getitem__(self, x):
        class Proxy:
            def __init__(self, my_field, x):
                self._my_field = my_field
                self._x = x

            def __getitem__(self, y):
                if y < 0 or y >= self._my_field.height:
                    return None
                if x < 0 or x >= self._my_field.width:
                    return None
                return self._my_field.layout[y][self._x]

            def __setitem__(self, y, item):
                if y < 0 or y >= self._my_field.height:
                    return
                if x < 0 or x >= self._my_field.width:
                    return
                self._my_field.layout[y][self._x] = item

        return Proxy(self, x)


field = Field(data)
beam_starts = [(x, 0) for x in range(field.width) if field[x][0] == "S"]
assert len(beam_starts) == 1
beam_start = beam_starts[0]


splits = 0
beams = [beam_start]
field[beam_start[0]][beam_start[1]] = "."
while beams:
    x, y = beams.pop()
    match field[x][y]:
        case None:
            pass
        case "|":
            pass
        case ".":
            field[x][y] = "|"
            beams.append((x, y + 1))
        case "^":
            if field[x + 1][y] == "." or field[x - 1][y] == ".":
                splits += 1
            beams.append((x + 1, y))
            beams.append((x - 1, y))

print(f"Problem 1: {splits}")


@lru_cache()
def timelines(beam):
    x, y = beam
    match field[x][y]:
        case None:
            return 1
        case "|":
            return timelines((x, y + 1))
        case ".":
            return timelines((x, y + 1))
        case "^":
            t_left = timelines((x - 1, y))
            t_right = timelines((x + 1, y))
            return t_left + t_right


print(f"Problem 2: {timelines(beam_start)}")
