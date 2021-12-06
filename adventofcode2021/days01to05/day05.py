from collections import defaultdict
from pprint import pprint
import re

from adventofcode2021.input_data import day05 as raw_data


def decomp(line):
    return re.findall("[0-9]*,[0-9]*", line)


def pair_of(string_tuple):
    return tuple(int(x) for x in string_tuple.split(","))


data = [tuple(pair_of(t) for t in decomp(l)) for l in raw_data.splitlines()]


def from_to(a, b):
    return range(min(a, b), max(a, b) + 1)


def generate_path(start, end, diagonals=False):
    x, y = start
    end_x, end_y = end

    if x == end_x:
        for i in from_to(y, end_y):
            yield x, i

    elif y == end_y:
        for i in from_to(x, end_x):
            yield i, y

    elif diagonals:
        # we want to always increment x for simplicity
        if x > end_x:
            x, end_x = end_x, x
            y, end_y = end_y, y

        climbing = 1 if end_y > y else -1

        for i in range(end_x - x + 1):
            yield x + i, y + climbing * i


def count_result(visited):
    return len(list(filter(lambda x: x > 1, visited.values())))


def visit(diagonals: bool):
    visited = defaultdict(int)
    for start, end in data:
        for pos in generate_path(start, end, diagonals):
            visited[pos] += 1
    return visited


def part1():
    return count_result(visit(False))


def part2():
    return count_result(visit(True))


if __name__ == "__main__":
    print(part1())
    print(part2())
