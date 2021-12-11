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


def update_and_append_if_flashing(grid, x, y, flashing_cells):
    grid[y][x] += 1
    if grid[y][x] >= 10:
        flashing_cells.append((x, y))


def update_neighbours(grid, coord):
    flashing = []
    for neighbour in neighbours(*coord):
        update_and_append_if_flashing(grid, *neighbour, flashing)
    return flashing


def trigger_flashing(grid, flashing_cells: list):
    seen = set()
    while flashing_cells:
        coord = flashing_cells.pop()
        if coord not in seen:
            seen.add(coord)
            flashing_neighbours = update_neighbours(grid, coord)
            flashing_cells.extend(x for x in flashing_neighbours if x not in seen)
    return seen


def simulate_step(grid):
    flashing_cells = []
    for coord in ((x, y) for x in range(10) for y in range(10)):
        update_and_append_if_flashing(grid, *coord, flashing_cells)

    flashed = trigger_flashing(grid, flashing_cells)

    for (x, y) in flashed:
        grid[y][x] = 0

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
