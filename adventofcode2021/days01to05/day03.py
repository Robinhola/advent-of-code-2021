from adventofcode2021.input_data import day03 as raw_data

from collections import defaultdict

data = raw_data.splitlines()
N = len(data[0])


def get_bits(lines):
    bits = defaultdict(list)
    for l in lines:
        for i in range(len(l)):
            bits[i].append(l[i])
    return bits


def reduce(bits: list):
    return (0, 1) if bits.count("0") > bits.count("1") else (1, 0)


def convert(bin):
    return sum((bin[N - 1 - i] * pow(2, i) for i in range(N)))


def part1():
    bits = get_bits(data)

    strongs, weaks = [], []
    for i in range(N):
        strong, weak = reduce(bits[i])
        strongs.append(strong)
        weaks.append(weak)

    return convert(strongs) * convert(weaks)


def filter_by(bit_index, value, iterable):
    return list(filter(lambda x: x[bit_index] == str(value), iterable))


def from_str_to_list(l: str):
    return [int(i) for i in l]


def multiply(a: list, b: list):
    return convert(from_str_to_list(a)) * convert(from_str_to_list(b))


def part2():
    filtered_by_most_common = list(data)
    filtered_by_least_common = list(data)

    for i in range(N):
        strong, _ = reduce(get_bits(filtered_by_most_common)[i])
        _, weak = reduce(get_bits(filtered_by_least_common)[i])

        if len(filtered_by_most_common) > 1:
            filtered_by_most_common = filter_by(i, strong, filtered_by_most_common)

        if len(filtered_by_least_common) > 1:
            filtered_by_least_common = filter_by(i, weak, filtered_by_least_common)

        if len(filtered_by_most_common) == len(filtered_by_least_common) == 1:
            return multiply(filtered_by_most_common[0], filtered_by_least_common[0])


if __name__ == "__main__":
    print(part1())
    print(part2())
