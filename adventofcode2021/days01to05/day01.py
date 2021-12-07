from typing import Generator
from adventofcode2021.input_data import day01 as data


def is_increasing(i: int):
    a, b = data[i - 1], data[i]
    return i > 0 and b > a


def is_sum_increasing(i: int):
    a = sum((data[i - 3], data[i - 2], data[i - 1]))
    b = sum((data[i - 2], data[i - 1], data[i]))
    return i > 2 and b > a


def count_values_based_on(predicate: callable):
    return len(tuple(filter(predicate, range(len(data)))))


if __name__ == "__main__":
    print(count_values_based_on(is_increasing))
    print(count_values_based_on(is_sum_increasing))
