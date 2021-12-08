from adventofcode2021.input_data import day08 as raw_data

# raw_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
# edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
# fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
# fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
# aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
# fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
# dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
# bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
# egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
# gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

data = raw_data.splitlines()


def read_output_values(line: str):
    return line.split(" ")


def part1():
    def is_len_unique(length: int):
        return length in (2, 3, 4, 7)

    count = 0
    for line in data:
        _, output_values = line.split(" | ")
        output_values = read_output_values(output_values)
        len_of_values = map(lambda x: len(x), output_values)
        count += len(list(filter(is_len_unique, len_of_values)))

    return count


def length_is(i: int):
    return lambda x: len(x) == i


def decode_patterns(patterns: list):
    # Read patterns
    """
    acedgfb: 8 ok
    cefabd: 9 ok
    cdfgeb: 6 ok
    cagedb: 0 ok
    cdfbe: 5 ok
    gcdfa: 2
    fbcad: 3 ok
    eafb: 4 ok
    dab: 7 ok
    ab: 1 ok
    """

    def unique_numbers():
        c_f = set(tuple(filter(length_is(2), patterns))[0])
        a_c_f = set(tuple(filter(length_is(3), patterns))[0])
        b_c_d_f = set(tuple(filter(length_is(4), patterns))[0])
        a_b_c_d_e_f_g = set(tuple(filter(length_is(7), patterns))[0])
        return c_f, a_c_f, b_c_d_f, a_b_c_d_e_f_g

    def find_6(one):
        possible_6 = [set(x) for x in tuple(filter(length_is(6), patterns))]
        for s in possible_6:
            if s.intersection(one) != one:
                return s

    def find_9(four, six):
        possible_9 = [
            set(x) for x in tuple(filter(length_is(6), patterns)) if set(x) != six
        ]
        for s in possible_9:
            if s.intersection(four) == four:
                return s

    def find_0(six, nine):
        possible_0 = [set(x) for x in tuple(filter(length_is(6), patterns))]
        for s in possible_0:
            if s != six and s != nine:
                return s

    def find_3(one):
        possible_3 = [set(x) for x in tuple(filter(length_is(5), patterns))]
        for s in possible_3:
            if s.intersection(one) == one:
                return s

    def find_5(six):
        possible_5 = [set(x) for x in tuple(filter(length_is(5), patterns))]
        for s in possible_5:
            if six.intersection(s) == s:
                return s

    def find_2(three, five):
        possible_0 = [set(x) for x in tuple(filter(length_is(5), patterns))]
        for s in possible_0:
            if s != three and s != five:
                return s

    one, seven, four, eight = unique_numbers()
    six = find_6(one)
    nine = find_9(four, six)
    zero = find_0(six, nine)
    three = find_3(one)
    five = find_5(six)
    two = find_2(three, five)

    numbers_as_sets = [zero, one, two, three, four, five, six, seven, eight, nine]
    numbers_as_tuples = [tuple(sorted(x)) for x in numbers_as_sets]
    return {numbers_as_tuples[i]: i for i in range(10)}


def decode_output_values(output_values, patterns):
    return [patterns[tuple(sorted(x))] for x in output_values]


def list_to_int(l):
    num_as_str = "".join(str(x) for x in l)
    return int(num_as_str)


def part2():
    result = 0
    for line in data:
        patterns, output_values = line.split(" | ")
        patterns, output_values = patterns.split(" "), output_values.split(" ")
        table = decode_patterns(patterns)
        values = decode_output_values(output_values, table)
        result += list_to_int(values)
    return result


if __name__ == "__main__":
    print(part1())
    print(part2())
