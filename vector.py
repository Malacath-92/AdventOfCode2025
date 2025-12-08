import math
from typing import NamedTuple


class Vector2(NamedTuple):
    x: int
    y: int

    def __add__(lhs, rhs):
        return Vector2(lhs.x + rhs.x, lhs.y + rhs.y)

    def __sub__(lhs, rhs):
        return Vector2(lhs.x - rhs.x, lhs.y - rhs.y)

    def __mul__(lhs, rhs: int):
        return Vector2(lhs.x * rhs, lhs.y * rhs)

    def __truediv__(lhs, rhs: int):
        return Vector2(lhs.x / rhs, lhs.y / rhs)

    @property
    def len(self):
        return math.sqrt(self.len_sqr)

    @property
    def len_sqr(self):
        return self.x * self.x + self.y * self.y

    def neighbours(self):
        return [
            self + Vector2(+1, +0),
            self + Vector2(-1, +0),
            self + Vector2(+0, +1),
            self + Vector2(+0, -1),
            self + Vector2(+1, +1),
            self + Vector2(-1, -1),
            self + Vector2(+1, -1),
            self + Vector2(-1, +1),
        ]


class Vector3(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(lhs, rhs):
        return Vector3(lhs.x + rhs.x, lhs.y + rhs.y, lhs.z + rhs.z)

    def __sub__(lhs, rhs):
        return Vector3(lhs.x - rhs.x, lhs.y - rhs.y, lhs.z - rhs.z)

    def __mul__(lhs, rhs: int):
        return Vector3(lhs.x * rhs, lhs.y - rhs.y, lhs.z * rhs.z)

    def __truediv__(lhs, rhs: int):
        return Vector3(lhs.x / rhs, lhs.y / rhs.y, lhs.z / rhs.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    @property
    def len(self):
        return math.sqrt(self.len_sqr)

    @property
    def len_sqr(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

def Vector(*args):
    if len(args) == 2:
        return Vector2(args[0], args[1])
    elif len(args) == 3:
        return Vector3(args[0], args[1], args[2])
    else:
        raise ValueError("Vector must be initialized with 2 or 3 arguments.")
