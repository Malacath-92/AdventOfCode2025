import aocd

import cli

from itertools import chain
from functools import reduce

sample_data = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """
data = sample_data if cli.sample else aocd.data
line_len = max(len(l) for l in data.splitlines())
data = "\n".join(l.ljust(line_len) for l in data.splitlines())
num_lines = len(data.splitlines())

lines = [l.split() for l in data.splitlines()]
problems = list(zip(*lines))


def compute_problem(problem):
    numbers = list(map(int, problem[:-1]))
    operator = problem[-1]
    if operator == "+":
        return sum(numbers)
    elif operator == "*":
        return reduce(lambda x, y: x * y, numbers)


solutions = list(map(compute_problem, problems))
print(f"Problem 1: {sum(solutions)}")


def split(lst, elem):
    lsts = []
    while elem in lst:
        i = lst.index(elem)
        lsts.append(lst[:i])
        lst = lst[i + 1 :]
    return lsts + [lst]


def de_cephalopodize(problem):
    numbers = ["".join(col[:-1]).strip() for col in problem]
    operator = problem[0][-1]
    return numbers + [operator]


problems = split(list(zip(*data.splitlines())), tuple(" " * num_lines))
problems = list(map(de_cephalopodize, problems))
solutions = list(map(compute_problem, problems))
print(f"Problem 2: {sum(solutions)}")
