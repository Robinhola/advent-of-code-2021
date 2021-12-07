from adventofcode2021.input_data import day02 as data

data = tuple((command, int(x)) for (command, x) in map(lambda l: l.split(" "), data))


def process_command(forward: int, depth: int, command: str, value: int):
    if command == "forward":
        return forward + value, depth

    if command == "down":
        return forward, depth + value

    if command == "up":
        return forward, depth - value


def process_command_aim(forward, depth, aim, command, value):
    if command == "forward":
        return forward + value, depth + aim * value, aim

    if command == "down":
        return forward, depth, aim + value

    if command == "up":
        return forward, depth, aim - value


def part1():
    forward, depth = 0, 0

    for command, x in data:
        forward, depth = process_command(forward, depth, command, x)

    return forward * depth


def part2():
    forward, depth, aim = 0, 0, 0

    for command, x in data:
        forward, depth, aim = process_command_aim(forward, depth, aim, command, x)

    return forward * depth


if __name__ == "__main__":
    print(part1())
    print(part2())
