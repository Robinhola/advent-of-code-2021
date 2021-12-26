from dataclasses import dataclass
from types import new_class
from typing import List
import math
import itertools

raw_data = """[1,1]
[2,2]
[3,3]
[4,4]"""

raw_data = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""


@dataclass
class SFNumber:
    index: int
    value: int
    position: bool  # False for Left, True for Right
    depth: int


def parse_line(line: str):
    numbers = []
    depth = 0
    is_right = []
    for character in line:
        if character == "[":
            depth += 1
            is_right.append(False)
        elif character == "]":
            depth -= 1
            is_right.pop()

        elif character.isnumeric():
            index = len(numbers)
            numbers.append(SFNumber(index, int(character), is_right[-1], depth))
        elif character == ",":
            is_right[-1] = True
    return numbers


def is_left(x: SFNumber):
    return x.position is False


def is_right(x: SFNumber):
    return x.position


def needs_work(numbers: List[SFNumber]):
    for x in numbers:
        if x.index >= len(numbers) - 1:
            break

        y = numbers[x.index + 1]

        if is_left(x) and is_right(y) and x.depth > 4:
            return x
        elif x.value > 9:
            return x
        elif y.value > 9:
            return y

    return None


def explode(x: SFNumber, numbers: List[SFNumber]):
    left = x
    right = numbers[x.index + 1]

    left_numbers = numbers[: left.index]
    right_numbers = numbers[right.index + 2 :]

    if left_numbers:
        left_numbers[-1].value += left.value

    if right_numbers:
        right_numbers[0].value += right.value

    for n in right_numbers:
        n.index -= 1

    should_be_right = False
    if left_numbers:
        should_be_right = left_numbers[-1].position

    new_number = SFNumber(x.index, 0, should_be_right, x.depth - 1)

    return left_numbers + [new_number] + right_numbers


def split(x: SFNumber, numbers: List[SFNumber]):
    new_left = SFNumber(x.index, math.floor(x.value / 2.0), False, x.depth + 1)
    new_right = SFNumber(x.index, math.ceil(x.value / 2.0), True, x.depth + 1)

    left_numbers = numbers[: x.index]
    right_numbers = numbers[x.index + 1 :]

    for n in right_numbers:
        n.index += 1

    return left_numbers + [new_left, new_right] + right_numbers


def addition(a: List[SFNumber], b: List[SFNumber]):
    for x in itertools.chain(a, b):
        x.depth += 1

    result = a + b

    x = needs_work(result)
    while x:
        if x.depth >= 4:
            result = explode(x, result)
        elif x.value > 9:
            result = split(x, result)
        x = needs_work(result)

    return result


def part1():
    number = None
    for l in raw_data.splitlines():
        if number == None:
            number = parse_line(l)
        else:
            number = addition(number, parse_line(l))
    return number


def part2():
    pass


if __name__ == "__main__":
    print(part1())
    print(part2())
