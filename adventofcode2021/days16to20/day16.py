from typing import Generator

raw_data = """A0016C880162017C3686B18A3D4780"""

translator_table = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def read_n_bits(generator, n):
    return "".join(next(generator) for _ in range(n))


def hexa_to_bits(packet: str):
    for l in packet:
        bits = translator_table[l]
        for b in bits:
            yield b


def read_header(generator):
    version = read_n_bits(generator, 3)
    typeId = read_n_bits(generator, 3)
    return version, typeId


def read_literal_value(generator):
    packet = ""
    continue_reading = True
    count = 6
    while continue_reading:
        prefix = next(generator)
        packet += read_n_bits(generator, 4)
        continue_reading = prefix == "1"
        count += 5

    extra_bits = 4 * (int(count / 4) + 1) - count
    for _ in range(extra_bits):
        next(generator)
    return packet


def from_binary_to_decimal(binary):
    return sum(int(b) * pow(2, i) for i, b in enumerate(reversed(binary)))


def read_next_packet(generator):
    try:
        version, typeId = read_header(generator)
    except RuntimeError:
        return []

    if typeId == "100":
        return [(version, typeId, read_literal_value(generator))]

    return [(version, typeId, ""), *read_operator(generator)]


def read_operator(generator):
    packets = []
    length_type_id = int(next(generator))
    if length_type_id == 0:
        total_length = from_binary_to_decimal(read_n_bits(generator, 15))
        i = 0
        while total_length - i > 6:
            for p in read_next_packet(generator):
                packets.append(p)
                i += len("".join(p))
                print(i, total_length)

    elif length_type_id == 1:
        number_of_sub_packets = from_binary_to_decimal(read_n_bits(generator, 11))
        for _ in range(number_of_sub_packets):
            packets.extend(read_next_packet(generator))

    else:
        raise RuntimeError(length_type_id)

    return packets


def part1():
    bits = hexa_to_bits(raw_data)
    packets = []
    next_packets = read_next_packet(bits)
    while next_packets:
        packets.extend(next_packets)
        next_packets = read_next_packet(bits)
        print(packets, next_packets)
    return sum(from_binary_to_decimal(v) for (v, _, _) in packets)


def part2():
    pass


if __name__ == "__main__":
    print(part1())
    print(part2())
