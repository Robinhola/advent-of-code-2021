from collections import Counter, defaultdict
from pprint import pprint
from typing import Sequence, Tuple

# Input
raw_data = """hl-WP
vl-fo
vl-WW
WP-start
vl-QW
fo-wy
WW-dz
dz-hl
fo-end
VH-fo
ps-vl
FN-dz
WP-ps
ps-start
WW-hl
end-QW
start-vl
WP-fo
end-FN
hl-QW
WP-dz
QW-fo
QW-dz
ps-dz"""

data = defaultdict(list)
for line in raw_data.splitlines():
    start, end = line.split("-")
    data[start].append(end)
    data[end].append(start)


def find_all_complete_paths(make_condition_from_path):
    completed_path = []
    paths = [["start"]]
    while paths:
        new_paths = []
        for p in paths:
            cave = p[-1]
            condition = make_condition_from_path(p)
            options = [x for x in data[cave] if condition(x)]
            for o in options:
                new = list(p)
                new.append(o)
                if o == "end":
                    completed_path.append(new)
                else:
                    new_paths.append(new)
        paths = new_paths
    return completed_path


def part1():
    def make_condition_from_path(path: list):
        already_seen = {x for x in path if x.islower()}

        def condition(cave):
            return cave not in already_seen

        return condition

    completed_paths = find_all_complete_paths(make_condition_from_path)

    return len(completed_paths)


def part2():
    def make_condition_from_path(path: list):
        counter = Counter(x for x in path if x.islower())

        def condition(cave):
            if cave == "start":
                return False
            if cave.islower() and 2 in counter.values() and counter[cave] >= 1:
                return False
            return True

        return condition

    completed_paths = find_all_complete_paths(make_condition_from_path)

    return len(completed_paths)


if __name__ == "__main__":
    print(part1())
    print(part2())
