import aocd

import cli

sample_data = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
data = sample_data if cli.sample else aocd.data

turns = [line for line in data.splitlines() if line]
turns = [(-1 if line[0] == 'L' else 1, int(line[1:])) for line in turns]

initial_pos = 50
pos = initial_pos


def next_pos(direction, distance):
    global pos
    pos = (pos + direction * distance) % 100
    return pos


positions = [next_pos(direction, distance) for direction, distance in turns]

print(f"Problem 1: {len([0 for p in positions if p == 0])}")


def clicks_for_turn(position, direction, distance):
    next_position = position + direction * distance
    clicks = abs(next_position) // 100
    extra_click = next_position <= 0 and position != 0
    return clicks + 1 if extra_click else clicks

clicks = [
    clicks_for_turn(position, direction, distance)
    for position, (direction, distance) in zip([initial_pos] + positions, turns)
]

print(f"Problem 2: {sum(clicks)}")
