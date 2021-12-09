import math

from adventofcode2021.input_data import day09 as raw_data


data = [[int(x) for x in l] for l in raw_data.splitlines()]


def access_data(x, y):
    return data[y][x]


def form_coordinates(x, y):
    return (x, y)


def add_if_valid(x, y, action: callable, container: list):
    if 0 <= x < len(data[0]) and 0 <= y < len(data):
        container.append(action(x, y))
    return container


def find_neighbours(x, y, action_on_x_y: callable):
    neighbours = []
    neighbours = add_if_valid(x - 1, y + 0, action_on_x_y, neighbours)
    neighbours = add_if_valid(x + 1, y + 0, action_on_x_y, neighbours)
    neighbours = add_if_valid(x + 0, y + 1, action_on_x_y, neighbours)
    neighbours = add_if_valid(x + 0, y - 1, action_on_x_y, neighbours)
    return neighbours


def find_low_points():
    def is_low_point(x, y):
        return data[y][x] < min(find_neighbours(x, y, access_data))

    return [
        (x, y)
        for x in range(len(data[0]))
        for y in range(len(data))
        if is_low_point(x, y)
    ]


def find_basin(coord: tuple, seen: set):
    x, y = coord
    basin = {coord}
    to_visit = [c for c in find_neighbours(x, y, form_coordinates)]

    while to_visit:
        x, y = c = to_visit.pop()

        if access_data(x, y) == 9 or c in seen:
            continue

        basin.add(c)
        seen.add(c)

        for c in find_neighbours(x, y, form_coordinates):
            to_visit.append(c)

    return basin


def part1():
    low_point_values = (data[y][x] for (x, y) in find_low_points())
    return sum(x + 1 for x in low_point_values)


def part2():
    low_points = find_low_points()
    seen = set(low_points)
    basins = list()

    for coord in low_points:
        basins.append(find_basin(coord, seen))

    largest_basins = sorted(len(x) for x in basins)[-3:]
    return math.prod(largest_basins)


if __name__ == "__main__":
    print(part1())
    print(part2())
