from input_data import day03 as raw_data

from collections import defaultdict

data = raw_data.splitlines()
N = len(data[0])


def part1():
    bits = defaultdict(list)
    for l in data:
        for i in range(len(l)):
            bits[i].append(l[i])

    def reduce(bits: list):
        return (0, 1) if bits.count("0") > bits.count("1") else (1, 0)

    strongs = []
    weaks = []
    for i in range(N):
        a, b = reduce(bits[i])
        strongs.append(a)
        weaks.append(b)

    def convert(bin):
        return sum((bin[N - 1 - i] * pow(2, i) for i in range(N)))

    return convert(strongs) * convert(weaks)


def part2():
    pass


if __name__ == "__main__":
    print(part1())
    print(part2())
