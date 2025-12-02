import aocd

import cli

import itertools

sample_data = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
data = sample_data if cli.sample else aocd.data

id_ranges = [tuple(id_range.split("-")) for id_range in data.split(",")]

def is_invalid_id(id):
    id_str = str(id)
    if len(id_str) % 2 == 0:
        half_len = len(id_str) // 2
        return id_str[:half_len] == id_str[half_len:]
    return False

all_ids = list(
    itertools.chain.from_iterable(
        [range(int(start), int(end) + 1) for start, end in id_ranges]
    )
)
invalid_ids = [id for id in all_ids if is_invalid_id(id)]

print(f"Problem 1: {sum(invalid_ids)}")
