from collections import Counter, defaultdict
from pprint import pprint
from typing import Sequence

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


def part1():
    completed_path = []
    paths = [["start"]]
    while paths:
        new_paths = []
        for p in paths:
            cave = p[-1]
            already_seen = {x for x in p if x.islower()}
            options = [x for x in data[cave] if x not in already_seen]
            for o in options:
                new = list(p)
                new.append(o)
                if o == "end":
                    completed_path.append(new)
                else:
                    new_paths.append(new)
        paths = new_paths
    return len(completed_path)


def part2():
    completed_path = []
    paths = [["start"]]
    while paths:
        new_paths = []
        for p in paths:
            cave = p[-1]
            count = Counter(x for x in p if x.islower())
            options = data[cave]
            for o in options:
                if o == "start":
                    continue

                if o.islower() and 2 in count.values() and count[o] >= 1:
                    continue

                new = list(p)
                new.append(o)
                if o == "end":
                    completed_path.append(new)
                else:
                    new_paths.append(new)
        paths = new_paths
    return len(completed_path)


if __name__ == "__main__":
    print(part1())
    print(part2())
