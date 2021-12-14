from collections import Counter, defaultdict

from adventofcode2021.input_data import day14 as raw_data

data = raw_data.splitlines()
polymer_template = data[0]
rules = {a: b for (a, b) in (x.split(" -> ") for x in data[2:])}


def pairs_of(template: str):
    for i in range(len(template) - 1):
        yield "".join((template[i], template[i + 1]))


def apply_n_steps(n):
    polymers = Counter(pairs_of(polymer_template))
    for i in range(n):
        new_polymers = defaultdict(int)
        for pair, count in polymers.items():
            for new_pair in [
                pair[0] + rules[pair],
                rules[pair] + pair[1],
            ]:
                new_polymers[new_pair] += count
        polymers = new_polymers
    return polymers


# I needed help for this one: mistake was to not abstract the problem and try to compute
# a 1_000_000_000_000 long string...
def difference_between_most_and_least_common(polymers):
    counts = [
        max(
            sum(count for (p1, _), count in polymers.items() if c == p1),
            sum(count for (_, p2), count in polymers.items() if c == p2),
        )
        for c in set("".join(polymers.keys()))
    ]

    return max(counts) - min(counts)


def part1():
    polymers = apply_n_steps(10)
    return difference_between_most_and_least_common(polymers)


def part2():
    polymers = apply_n_steps(40)
    return difference_between_most_and_least_common(polymers)


if __name__ == "__main__":
    print(part1())
    print(part2())
