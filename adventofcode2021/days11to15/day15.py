from collections import defaultdict
import heapq

from adventofcode2021.input_data import day15 as raw_data

# raw_data = """1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581"""

data = [list(map(int, line)) for line in raw_data.splitlines()]

len_x = len(data[0])
len_y = len(data)


def cost(x, y):
    return data[y][x]


def neighbours(x, y):
    return [
        (a, b)
        for (a, b) in ((x + 1, y), (x, y + 1))
        if 0 <= a < len_x and 0 <= b < len_y
    ]


def big_cave_cost(x, y):
    value = data[y % len_y][x % len_x]
    value += int(y / len_y) + int(x / len_x)
    value = value % 9
    value = 9 if value == 0 else value
    return value


def big_cave_neighbours(x, y):
    return (
        (a, b)
        for (a, b) in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))
        if 0 <= a < 5 * len_x and 0 <= b < 5 * len_y
    )


def djikstra(neighbours_fn: callable, cost_fn: callable, goal):
    to_visit: list = [(0, (0, 0))]
    distance: dict = defaultdict(lambda: float("inf"))
    distance[(0, 0)] = 0

    visited = {(0, 0)}

    while to_visit:
        risk, (x, y) = heapq.heappop(to_visit)
        if (x, y) == goal:
            return risk

        for neighbour in neighbours_fn(x, y):
            if neighbour in visited:
                continue
            visited.add(neighbour)
            new_value = risk + cost_fn(*neighbour)
            if new_value < distance[neighbour]:
                distance[neighbour] = new_value
                heapq.heappush(to_visit, (new_value, neighbour))


def part1():
    return djikstra(neighbours, cost, (len_x - 1, len_y - 1))


def part2():
    return djikstra(big_cave_neighbours, big_cave_cost, (len_x * 5 - 1, len_y * 5 - 1))


if __name__ == "__main__":
    print(part1())
    print(part2())
