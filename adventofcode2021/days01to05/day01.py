from adventofcode2021.input_data import day01 as data


def part1():
    count = 0
    for i in range(len(data)):
        if i == 0:
            continue
        a, b = data[i - 1], data[i]
        if a < b:
            count += 1
    return count


def part2():
    count = 0
    for i in range(len(data)):
        a = sum((data[i - 3], data[i - 2], data[i - 1]))
        b = sum((data[i - 2], data[i - 1], data[i]))
        if a < b:
            count += 1
    return count


if __name__ == "__main__":
    print(part1())
    print(part2())
