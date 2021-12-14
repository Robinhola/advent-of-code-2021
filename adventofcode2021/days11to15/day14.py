from collections import Counter

from adventofcode2021.input_data import day14 as raw_data

data = raw_data.splitlines()
polymer_template = data[0]
pair_insertion_rules = {a: b for (a, b) in (x.split(" -> ") for x in data[2:])}


def pairs_of(template: str):
    for i in range(len(template) - 1):
        yield "".join((template[i], template[i + 1]))


def apply_step(template: str):
    new_template = []
    for pair in pairs_of(template):
        new_template.append(pair[0])
        if pair in pair_insertion_rules:
            new_template.append(pair_insertion_rules[pair])
    new_template.append(pair[1])
    return "".join(new_template)


def apply_n_steps(n):
    template = polymer_template
    for i in range(n):
        print("step", i)
        template = apply_step(template)
    return template


def difference_between_most_and_least_common(template):
    counter = Counter(template)
    most_common = counter.most_common(1)[0][1]
    least_common = counter.most_common()[-1][1]
    return most_common - least_common


def part1():
    template = apply_n_steps(10)
    return difference_between_most_and_least_common(template)


def part2():
    template = apply_n_steps(40)
    return difference_between_most_and_least_common(template)


if __name__ == "__main__":
    print(part1())
    print(part2())
