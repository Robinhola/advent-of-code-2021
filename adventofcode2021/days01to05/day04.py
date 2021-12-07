import re
from pprint import pprint
from collections import defaultdict

from adventofcode2021.input_data import day04 as raw_data


N = 5

raw_data_lines = raw_data.splitlines()

input = raw_data_lines[0].split(",")

boards = [
    [re.split("\s+", l.strip()) for l in b]
    for b in [raw_data_lines[i : i + N] for i in range(2, len(raw_data_lines), N + 1)]
]


def generate_numbers():
    numbers = defaultdict(dict)
    for i in range(len(boards)):
        for y in range(N):
            for x in range(N):
                n = boards[i][y][x]
                numbers[n][i] = (x, y)
    return numbers


def all_numbers_of(board: list):
    return {number for line in board for number in line}


def sum_of_unmarked_numbers(board: list, marked_numbers: list):
    A = all_numbers_of(board)
    B = set(marked_numbers)
    return sum(int(v) for v in A.difference(B))


def part1():
    # remember where each number is (board, row, column)
    # remember the state of each column and each row
    # return which board has won
    numbers = generate_numbers()

    marked_numbers_of = defaultdict(list)
    board_counts_x_of = defaultdict(lambda: defaultdict(int))
    board_counts_y_of = defaultdict(lambda: defaultdict(int))

    def update(b: int, x: int, y: int):
        board_counts_x_of[b][x] += 1
        board_counts_y_of[b][y] += 1
        marked_numbers_of[b].append(n)
        return board_counts_x_of[b][x] == N or board_counts_y_of[b][y] == N

    for n in input:
        targets = numbers[n]
        for b in targets:
            if update(b, *targets[b]):
                # we stop as soon as a board has won
                return int(n) * sum_of_unmarked_numbers(boards[b], marked_numbers_of[b])


def part2():
    numbers = generate_numbers()

    marked_numbers_of = defaultdict(list)
    board_counts_x_of = defaultdict(lambda: defaultdict(int))
    board_counts_y_of = defaultdict(lambda: defaultdict(int))

    def update(b: int, x: int, y: int):
        board_counts_x_of[b][x] += 1
        board_counts_y_of[b][y] += 1
        marked_numbers_of[b].append(n)
        return board_counts_x_of[b][x] == N or board_counts_y_of[b][y] == N

    has_already_won = set()
    won_boards_count = 0

    for n in input:
        targets = numbers[n]
        for b in targets:
            if update(b, *targets[b]) and b not in has_already_won:
                has_already_won.add(b)
                won_boards_count += 1

                if won_boards_count == len(boards):
                    # we only stop when all boards have won
                    return int(n) * sum_of_unmarked_numbers(
                        boards[b], marked_numbers_of[b]
                    )


if __name__ == "__main__":
    print(part1())
    print(part2())
