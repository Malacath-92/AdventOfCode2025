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


def max_joltage(bank, joltage_size):
    def next_battery(bank):
        num_batteries = len(bank)

        next_battery_index = 0
        for i in range(1, num_batteries):
            battery = bank[i]
            if battery > bank[next_battery_index]:
                next_battery_index = i

        return next_battery_index

    max_joltage = 0
    used_bank = 0
    for i in range(joltage_size):
        remaining = joltage_size - i - 1
        available_bank = bank[used_bank:-remaining] if remaining else bank[used_bank:]
        next_battery_index = next_battery(available_bank)
        max_joltage = max_joltage * 10 + available_bank[next_battery_index]
        used_bank += next_battery_index + 1
    return max_joltage


joltages = [max_joltage(bank, 2) for bank in banks]

print(f"Problem 1: {sum(joltages)}")


joltages = [max_joltage(bank, 12) for bank in banks]

print(f"Problem 2: {sum(joltages)}")
