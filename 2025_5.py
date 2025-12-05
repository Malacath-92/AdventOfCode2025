import aocd

import cli

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

# MemoryError
# all_fresh = set(
#     itertools.chain.from_iterable(map(lambda x: list(range(x[0], x[1] + 1)), fresh_ranges))
# )


# Reduce ranges
def reduce_ranges():
    reduced_ranges = []
    for i in range(len(fresh_ranges) - 1):
        if fresh_ranges[i] is None:
            continue

        for j in range(i + 1, len(fresh_ranges)):
            if fresh_ranges[j] is None:
                continue

            min_i = fresh_ranges[i][0]
            max_i = fresh_ranges[i][1]
            min_j = fresh_ranges[j][0]
            max_j = fresh_ranges[j][1]
            if (
                min_i <= min_j <= max_i
                or min_j <= min_i <= max_j
                or min_i <= max_j <= max_i
                or min_j <= max_i <= max_j
            ):
                fresh_ranges[i][0] = min(min_i, min_j)
                fresh_ranges[i][1] = max(max_i, max_j)
                fresh_ranges[j] = None
                reduced_ranges.append(j)

    for i in reversed(sorted(reduced_ranges)):
        assert fresh_ranges[i] is None
        del fresh_ranges[i]

    return len(reduced_ranges) > 0


while reduce_ranges():
    pass

range_lengths = list(map(lambda x: x[1] - x[0] + 1, fresh_ranges))
num_fresh = sum(range_lengths)

print("Problem 1:", num_fresh)
