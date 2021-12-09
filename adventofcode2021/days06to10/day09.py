import math

from adventofcode2021.input_data import day09 as raw_data


data = [[int(x) for x in l] for l in raw_data.splitlines()]
LEN_X = len(data[0])
LEN_Y = len(data)


def access_data(x, y):
    return data[y][x]


def form_coordinates(x, y):
    return (x, y)


def is_valid(x, y):
    return 0 <= x < LEN_X and 0 <= y < LEN_Y


def find_neighbours(x, y, action_on_x_and_y: callable):
    return [
        action_on_x_and_y(*coord)
        for coord in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        if is_valid(*coord)
    ]


def is_low_point(x, y):
    return access_data(x, y) < min(find_neighbours(x, y, access_data))


def find_low_points():
    return [(x, y) for x in range(LEN_X) for y in range(LEN_Y) if is_low_point(x, y)]


def find_basin(coord: tuple, seen: set):
    basin = set()
    to_visit = [coord]
    while to_visit:
        coord = to_visit.pop()
        seen.add(coord)
        basin.add(coord)
        to_visit.extend(
            new_coord
            for new_coord in find_neighbours(*coord, form_coordinates)
            if access_data(*new_coord) != 9 and new_coord not in seen
        )
    return basin


def part1():
    low_point_values = (access_data(*coord) for coord in find_low_points())
    risk_values = (x + 1 for x in low_point_values)
    return sum(risk_values)


def part2():
    low_points = find_low_points()
    already_seen = set()
    basins = (find_basin(coord, already_seen) for coord in low_points)
    largest_basins = sorted(len(x) for x in basins)[-3:]
    return math.prod(largest_basins)


if __name__ == "__main__":
    print(part1())
    print(part2())
