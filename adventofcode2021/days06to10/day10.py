from adventofcode2021.input_data import day10 as raw_data

data = raw_data.splitlines()

opening_correspondence = {
    "[": "]",
    "{": "}",
    "(": ")",
    "<": ">",
}

point = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

value_of = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def find_corruption(line):
    expecting = []
    for c in line:
        if c in opening_correspondence:
            expecting.append(opening_correspondence[c])
        elif c == expecting[-1]:
            expecting.pop()
        else:
            return c
    return None


def find_incomplete(line):
    expecting = []
    for c in line:
        if c in opening_correspondence:
            expecting.append(opening_correspondence[c])
        elif c == expecting[-1]:
            expecting.pop()
        else:
            return []
    return list(reversed(expecting))


def calculate_score(ending_characters: list):
    score = 0
    for c in ending_characters:
        score *= 5
        score += value_of[c]
    return score


def part1():
    corrupted_letters = map(find_corruption, data)
    return sum(point[c] for c in corrupted_letters if c)


def part2():
    scores = sorted(calculate_score(l) for l in map(find_incomplete, data) if l)
    middle_index = int(len(scores) / 2)
    return scores[middle_index]


if __name__ == "__main__":
    print(part1())
    print(part2())
