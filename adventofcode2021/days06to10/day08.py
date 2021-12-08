from adventofcode2021.input_data import day08 as raw_data

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
    def extract_numbers_of_length(i: int):
        return tuple(filter(length_is(i), patterns))

    def unique_numbers():
        c_f = set(extract_numbers_of_length(2)[0])
        a_c_f = set(extract_numbers_of_length(3)[0])
        b_c_d_f = set(extract_numbers_of_length(4)[0])
        a_b_c_d_e_f_g = set(extract_numbers_of_length(7)[0])
        return c_f, a_c_f, b_c_d_f, a_b_c_d_e_f_g

    def find_0_6_9(one, four):
        possibilities = [set(x) for x in extract_numbers_of_length(6)]
        for s in possibilities:
            if s.intersection(one) != one:
                six = s
            elif s.intersection(four) == four:
                nine = s
            else:
                zero = s
        return zero, six, nine

    def find_2_3_5(one, six):
        possibilities = [set(x) for x in extract_numbers_of_length(5)]
        for s in possibilities:
            if s.intersection(one) == one:
                three = s
            elif six.intersection(s) == s:
                five = s
            else:
                two = s
        return two, three, five

    one, seven, four, eight = unique_numbers()
    zero, six, nine = find_0_6_9(one, four)
    two, three, five = find_2_3_5(one, six)

    numbers_as_sets = [zero, one, two, three, four, five, six, seven, eight, nine]
    numbers_as_tuples = [tuple(sorted(x)) for x in numbers_as_sets]
    return {numbers_as_tuples[i]: i for i in range(10)}


def decode_output_values(output_values: list, pattern_table: dict):
    return [pattern_table[tuple(sorted(x))] for x in output_values]


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
