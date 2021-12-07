from collections import Counter

from adventofcode2021.input_data import day07 as raw_data

data = [int(x) for x in raw_data.split(",")]

crabs_position = Counter(data)


def sum_of_n_numbers(n: int):
    return int((n + 1) * n / 2)


def calculate_cost_from(start: int):
    def cost_for(key_pair: tuple):
        position, number = key_pair
        return abs(start - position) * number

    return sum(map(cost_for, crabs_position.items()))


def calculate_cost_from_with_increase(start: int):
    def cost_for(key_pair: tuple):
        position, number = key_pair
        return sum_of_n_numbers(abs(start - position)) * number

    return sum(map(cost_for, crabs_position.items()))


def part1():
    start_points = crabs_position.keys()
    return min(map(calculate_cost_from, start_points))


def part2():
    start_points = range(max(crabs_position))
    return min(map(calculate_cost_from_with_increase, start_points))


if __name__ == "__main__":
    # Giant Whale!
    print(part1())
    print(part2())
