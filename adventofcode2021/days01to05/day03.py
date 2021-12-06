from input_data import day03 as raw_data

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

    strongs = []
    weaks = []
    for i in range(N):
        a, b = reduce(bits[i])
        strongs.append(a)
        weaks.append(b)

    return convert(strongs) * convert(weaks)


def filter_by(bit_number, value, iterable):
    return list(filter(lambda x: x[bit_number] == str(value), iterable))


def part2():
    filtered_by_most_common = list(data)
    filtered_by_least_common = list(data)

    for i in range(N):
        most_common, _ = reduce(get_bits(filtered_by_most_common)[i])
        _, least_common = reduce(get_bits(filtered_by_least_common)[i])

        if len(filtered_by_most_common) > 1:
            filtered_by_most_common = filter_by(i, most_common, filtered_by_most_common)

        if len(filtered_by_least_common) > 1:
            filtered_by_least_common = filter_by(
                i, least_common, filtered_by_least_common
            )

        if len(filtered_by_most_common) == len(filtered_by_least_common) == 1:
            break

    def from_str_to_list(l):
        return [int(i) for i in l]

    a = from_str_to_list(filtered_by_most_common[0])
    b = from_str_to_list(filtered_by_least_common[0])

    a = convert(a)
    b = convert(b)

    return a * b


if __name__ == "__main__":
    print(part1())
    print(part2())
