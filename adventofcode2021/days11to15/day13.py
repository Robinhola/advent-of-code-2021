from adventofcode2021.input_data import day13 as raw_data

data = raw_data.splitlines()
dots = [
    tuple(int(l) for l in x.split(","))
    for x in data
    if x and not x.startswith("fold along")
]
folding_instructions = [
    (a, int(b))
    for (a, b) in (
        tuple(x.split("fold along ")[1].split("="))
        for x in data
        if x.startswith("fold along")
    )
]


def transform(folding_direction, folding_parallel, x, y):
    def offset(value):
        offset = value - folding_parallel
        return folding_parallel - offset

    if folding_direction == "x" and x > folding_parallel:
        return (offset(x), y)

    if folding_direction == "y" and y > folding_parallel:
        return (x, offset(y))

    return (x, y)


def part1():
    folding_direction = folding_instructions[0][0]
    folding_parallel = folding_instructions[0][1]
    dots_after_first_fold = {
        transform(folding_direction, folding_parallel, *coord) for coord in dots
    }
    return len(dots_after_first_fold)


def part2():
    dots_after_folding = set(dots)
    for fold in folding_instructions:
        dots_after_folding = {transform(*fold, *coord) for coord in dots_after_folding}
    return dots_after_folding


def print_capital_letters(dots_after_folding):
    paper = [[" "] * (5 * 8 - 1) for _ in range(6)]
    for (x, y) in dots_after_folding:
        paper[y][x] = "#"
    for l in paper:
        print("".join(l))


if __name__ == "__main__":
    print(part1())
    print_capital_letters(part2())
