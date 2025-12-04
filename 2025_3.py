import aocd

import cli

import functools
import itertools

sample_data = """\
987654321111111
811111111111119
234234234234278
818181911112111"""
data = sample_data if cli.sample else aocd.data

banks = [list(map(int, bank)) for bank in data.splitlines()]

def max_joltage(bank):
    num_batteries = len(bank)
    max_joltage = 0
    for i in range(num_batteries):
        left_battery = bank[i] * 10
        if max_joltage % 10 >= left_battery:
            continue

        for j in range(i + 1, num_batteries):
            right_battery = bank[j]
            joltage = left_battery + right_battery
            max_joltage = max(max_joltage, joltage)

    return max_joltage


joltages = [max_joltage(bank) for bank in banks]

print(f"Problem 1: {sum(joltages)}")
