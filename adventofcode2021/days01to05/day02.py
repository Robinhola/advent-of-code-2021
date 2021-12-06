from adventofcode2021.input_data import day02 as data


def part1():
    forward = 0
    depth = 0

    for l in data:
        command, x = l.split(" ")
        value = int(x)

        if command == "forward":
            forward += value
        if command == "down":
            depth += value
        if command == "up":
            depth -= value

    return forward * depth


def part2():
    forward = 0
    depth = 0
    aim = 0

    for l in data:
        command, x = l.split(" ")
        value = int(x)

        if command == "forward":
            forward += value
            depth += aim * value
        if command == "down":
            aim += value
        if command == "up":
            aim -= value

    return forward * depth


if __name__ == "__main__":
    print(part1())
    print(part2())
