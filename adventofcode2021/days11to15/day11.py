# example
# raw_data = """5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526"""

raw_data = """1224346384
5621128587
6388426546
1556247756
1451811573
1832388122
2748545647
2582877432
3185643871
2224876627"""


def get(grid, x, y):
    return grid[y][x]


def set_value(grid, x, y, value):
    grid[y][x] = value


def make_grid():
    return [[int(x) for x in l] for l in raw_data.splitlines()]


def neighbours(x, y):
    def is_valid(x, y):
        return 0 <= x < 10 and 0 <= y < 10

    return (
        coord
        # fmt: off
        for coord in (
            (x - 1, y - 1), (x - 0, y - 1), (x + 1, y - 1),
            (x - 1, y - 0), (x - 0, y - 0), (x + 1, y - 0),
            (x - 1, y + 1), (x - 0, y + 1), (x + 1, y + 1),
        )
        # fmt: on
        if is_valid(*coord)
    )


def update_neighbours(grid, coord):
    flashing = []
    for neighbour in neighbours(*coord):
        x, y = neighbour
        value = get(grid, x, y) + 1
        set_value(grid, x, y, value)
        if value >= 10:
            flashing.append(neighbour)
    return flashing


def trigger_flashing(grid, flashing_cells: list):
    seen = set()
    while flashing_cells:
        coord = flashing_cells.pop()

        if coord in seen:
            continue

        seen.add(coord)

        flashing_neighbours = update_neighbours(grid, coord)
        flashing_cells.extend(x for x in flashing_neighbours if x not in seen)

    return seen


def simulate_step(grid):
    flashing_cells = []

    for (x, y) in ((x, y) for x in range(10) for y in range(10)):
        value = get(grid, x, y) + 1
        set_value(grid, x, y, value)
        if value == 10:
            flashing_cells.append((x, y))

    flashed = trigger_flashing(grid, flashing_cells)

    for coord in flashed:
        set_value(grid, *coord, 0)

    return len(flashed)


def part1():
    grid = make_grid()
    return sum(simulate_step(grid) for _ in range(100))


def part2():
    grid = make_grid()
    step = 1

    while simulate_step(grid) != 100:
        step += 1

    return step


if __name__ == "__main__":
    print(part1())
    print(part2())
