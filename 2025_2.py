import aocd

import cli

import functools
import itertools

sample_data = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
data = sample_data if cli.sample else aocd.data

id_ranges = [tuple(id_range.split("-")) for id_range in data.split(",")]
all_ids = list(
    itertools.chain.from_iterable(
        [range(int(start), int(end) + 1) for start, end in id_ranges]
    )
)


def is_invalid_id(id):
    id_str = str(id)
    if len(id_str) % 2 == 0:
        half_len = len(id_str) // 2
        return id_str[:half_len] == id_str[half_len:]
    return False


invalid_ids = [id for id in all_ids if is_invalid_id(id)]

print(f"Problem 1: {sum(invalid_ids)}")


@functools.lru_cache
def divisors(n):
    def divisors_impl(n):
        yield n
        for i in range(2, int(n // 2 + 1)):
            if n % i == 0:
                yield int(i)
    return tuple(divisors_impl(n))


def is_invalid_id(id):
    id_str = str(id)
    if len(id_str) < 2:
        return False
    for div in divisors(len(id_str)):
        frac_len = len(id_str) // div
        if id_str == id_str[:frac_len] * div:
            return True
    return False


invalid_ids = [id for id in all_ids if is_invalid_id(id)]

print(f"Problem 2: {sum(invalid_ids)}")
