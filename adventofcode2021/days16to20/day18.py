from dataclasses import dataclass
import math
from collections import defaultdict
from typing import List, Optional


@dataclass
class SnailNumberMember:
    value: int
    index: int
    depth: int
    is_left: bool


def read_number(line: str):
    full_number = []
    index = 0
    depth = 0
    is_left = True
    for character in line:
        if character.isnumeric():
            full_number.append(
                SnailNumberMember(
                    value=int(character), index=index, depth=depth, is_left=is_left
                )
            )
            index += 1
        elif character == "[":
            is_left = True
            depth += 1
        elif character == "]":
            depth -= 1
        elif character == ",":
            is_left = False

    return full_number


def explode(target: SnailNumberMember, full_number: list):
    left = full_number[target.index]
    right = full_number[target.index + 1]
    is_left = None

    if left.index > 0:
        previous = full_number[left.index - 1]
        previous.value += left.value
        is_left = previous.depth != 4 or not previous.is_left
    else:
        is_left = True

    if right.index + 1 < len(full_number):
        full_number[right.index + 1].value += right.value

    for i in range(right.index + 1, len(full_number)):
        full_number[i].index -= 1

    left.value = 0
    left.depth -= 1
    left.is_left = is_left

    return full_number[: right.index] + full_number[right.index + 1 :]


def split(target: SnailNumberMember, full_number: list):
    left = SnailNumberMember(
        value=math.floor(target.value / 2.0),
        index=target.index,
        depth=target.depth + 1,
        is_left=True,
    )

    right = SnailNumberMember(
        value=math.ceil(target.value / 2.0),
        index=target.index + 1,
        depth=target.depth + 1,
        is_left=False,
    )

    for i in range(target.index + 1, len(full_number)):
        full_number[i].index += 1

    result = (
        full_number[: target.index] + [left, right] + full_number[target.index + 1 :]
    )

    return result


def clean_up(full_number: list):
    done = False
    while not done:
        done = True
        for x in (a for a in full_number if a.depth > 4):
            full_number = explode(x, full_number)
            done = False
            break

        if not done:
            continue

        for x in (a for a in full_number if a.value > 9):
            full_number = split(x, full_number)
            done = False
            break

    return full_number


def addition(left: list, right: list):
    for x in left:
        x.depth += 1
    for x in right:
        x.depth += 1
        x.index += len(left)
    return clean_up(left + right)


def compute_from_track(track, value):
    tmp = value
    for coeff in (3 if a else 2 for a in track):
        tmp *= coeff
    return tmp


def magnitude(full_number: List[SnailNumberMember]):
    track = []
    depth = 0
    result = 0

    for x in full_number:
        if x.depth > depth:
            offset = x.depth - depth
            track.extend([True] * offset)
        elif x.depth < depth:
            track = track[: -(depth - x.depth)]

        track[-1] = x.is_left
        result += compute_from_track(track, x.value)
        if x.is_left:
            depth = x.depth
        else:
            depth = x.depth - 1
            track.pop()
            for i in range(len(track)):
                if track[-1 - i]:
                    track[-1 - i] = False
                    break
                else:
                    track[-1 - i] = True

    return result


from adventofcode2021.input_data import day18 as raw_data


def part1():
    a = None
    for l in raw_data.splitlines():
        if a == None:
            a = read_number(l)
        else:
            a = addition(a, read_number(l))
    return magnitude(a)


def part2():
    numbers = raw_data.splitlines()
    results = []

    for i, n in enumerate(numbers):
        for c in numbers[i + 1 :]:
            first = magnitude(addition(read_number(n), read_number(c)))
            second = magnitude(addition(read_number(c), read_number(n)))
            results.append(max(first, second))

    return max(results)


if __name__ == "__main__":
    print(part1())
    print(part2())
