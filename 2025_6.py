import aocd

import cli

from functools import reduce

sample_data = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """
data = sample_data if cli.sample else aocd.data

lines = [l.split() for l in data.splitlines()]
problems = list(zip(*lines))

def compute_problem(problem):
    numbers = list(map(int, problem[:-1]))
    operator = problem[-1]
    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        return reduce(lambda x, y: x * y, numbers)

solutions = list(map(compute_problem, problems))

print(f"Problem 1: {sum(solutions)}")